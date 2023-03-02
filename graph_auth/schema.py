from smtplib import SMTPException

import graphene
import graphql_jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import BadSignature, SignatureExpired
from django.db import IntegrityError
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import (login_required, superuser_required,
                                    token_auth)


from .constants import Messages, TokenAction
from .exceptions import (EmailAlreadyInUse, TokenScopeError,
                         UserAlreadyVerified, UserNotVerified)
from .base import (BaseRegister, PasswordResetBase,
                           ResendActivationEmailBase,
                           SendPasswordResetEmailBase, VerifyAccountBase)
from .models import UserStatus
from .shortcuts import get_user_by_email
from .signals import user_registered, user_verified
from .utils import get_token_payload, revoke_user_refresh_token

UserModel = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = "__all__"
        filter_fields = ["email", "username", "is_active", "is_staff", "is_superuser"]
        interfaces = (relay.Node,)


class UserStatusType(DjangoObjectType):
    class Meta:
        model = UserStatus
        fields = "__all__"
        filter_fields = ["user", "verified", "archived"]
        interfaces = (relay.Node,)


class AuthQuery(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    userstatus = DjangoFilterConnectionField(UserStatusType)

    @login_required
    # TODO: Create a @verification_required
    def resolve_me(root, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_user(root, info, id, **kwargs):
        return UserModel.objects.get(pk=id)

    @superuser_required
    def resolve_userstatus(self, info, **kwargs):
        return UserStatus.objects.all()


class Register(BaseRegister):

    user = graphene.Field(UserType, description="A newly created user.")

    class Meta:
        description = "Register a new user."
        model = UserModel

    @classmethod
    @token_auth
    def login_on_register(cls, root, info, **kwargs):
        """
        Login the User upon Registration
        Sets the HTTP Cookie with the help of @token_auth
        """
        return cls()

    @classmethod
    def perform_mutation(cls, root, info, **kwargs):
        """
        register(
            email: String!
            username: String!
            password: String!
        ): Register

        """
        try:
            email = kwargs.get("email")
            password = kwargs.get("password")
            username = kwargs.get("username")
            # clean email
            UserStatus.clean_email(email)
            # create user
            user = UserModel.objects.create_user(
                email=email, password=password, username=username
            )

            send_activation = settings.SEND_ACTIVATION_EMAIL is True and email
            if send_activation:
                user.status.send_activation_email(info)

            user_registered.send(sender=cls, user=user)
            if settings.ALLOW_LOGIN_NOT_VERIFIED:
                payload = cls.login_on_register(root, info, **kwargs)
                print("Pay", payload)

            return cls(
                success=True,
                errors=None,
                user=user,
            )
        except IntegrityError:
            return cls(
                success=False,
                errors=[Messages.USERNAME_IN_USE],
                user=None,
            )
        except EmailAlreadyInUse:
            return cls(
                success=False,
                errors=[Messages.EMAIL_IN_USE],
                user=None,
            )
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except Exception as e:
            # TODO
            # notify_admins.apply_async(
            #     args=[
            #         "Registration Mutation Exception",
            #         "Exception details: %s" % str(e),
            #     ],
            #     countdown=10,
            # )
            print("Exception details: %s" % str(e))
            return cls(
                success=False,
                errors=[Messages.SERVER_ERROR],
                user=None,
            )


class VerifyAccount(VerifyAccountBase):
    class Meta:
        description = "Verify the user's email address with token."

    @classmethod
    def perform_mutation(cls, root, info, **kwargs):
        """
        verifyAccount(
            token: String!
        ): VerifyAccount
        """
        try:
            token = kwargs.get("token")
            UserStatus.verify(token)
            return cls(
                success=True,
                errors=None,
            )
        except SignatureExpired:
            return cls(
                success=False,
                errors=[Messages.EXPIRED_TOKEN],
            )
        except (BadSignature, TokenScopeError):
            return cls(
                success=False,
                errors=[Messages.INVALID_TOKEN],
            )
        except UserAlreadyVerified:
            return cls(
                success=False,
                errors=[Messages.ALREADY_VERIFIED],
            )
        except Exception as e:
            # notify_admins.apply_async(
            #     args=[
            #         "Verification Mutation Exception",
            #         "Exception details: %s" % str(e),
            #     ],
            #     countdown=10,
            # )
            print("Exception details: %s" % str(e))
            return cls(
                success=False,
                errors=[Messages.SERVER_ERROR],
                user=None,
            )


class ResendActivationEmail(ResendActivationEmailBase):
    class Meta:
        description = "Resend the activation email."

    @classmethod
    # TODO @login_required
    def perform_mutation(cls, root, info, **kwargs):
        """
        resendActivationEmail(
            email: String!
        ): ResendActivationEmail
        """
        try:
            email = kwargs.get("email")
            user = get_user_by_email(email)
            user.status.resend_activation_email(info)
            return cls(
                success=True,
                errors=None,
            )
        except ObjectDoesNotExist:
            # even if user is not registred
            return cls(
                success=True,
                errors=None,
            )
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except UserAlreadyVerified:
            return cls(success=False, errors=Messages.ALREADY_VERIFIED)
        except Exception as e:
            # notify_admins.apply_async(
            #     args=[
            #         "ResendActivation Mutation Exception",
            #         "Exception details: %s" % str(e),
            #     ],
            #     countdown=10,
            # )
            print("Exception details: %s" % str(e))
            return cls(
                success=False,
                errors=[Messages.SERVER_ERROR],
                user=None,
            )


class SendPasswordResetEmail(SendPasswordResetEmailBase):
    class Meta:
        description = "Send a password reset email."

    @classmethod
    def perform_mutation(cls, root, info, **kwargs):
        """
        sendPasswordResetEmail(
            email: String!
        ): SendPasswordResetEmail
        """
        try:
            email = kwargs.get("email")
            user = get_user_by_email(email)
            # If user not verified
            if not user.status.verified:
                raise UserNotVerified
            user.status.send_password_reset_email(info, [email])
            return cls(
                success=True,
                errors=None,
            )
        except ObjectDoesNotExist:
            # even if user is not registred
            return cls(
                success=True,
                errors=None,
            )
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
        except UserNotVerified:
            user = get_user_by_email(email)
            user.status.resend_activation_email(info)
            return cls(
                success=False,
                errors=Messages.NOT_VERIFIED_PASSWORD_RESET,
            )
        except Exception as e:
            # notify_admins.apply_async(
            #     args=[
            #         "SendPasswordReset Mutation Exception",
            #         "Exception details: %s" % str(e),
            #     ],
            #     countdown=10,
            # )
            print("Exception details: %s" % str(e))
            return cls(
                success=False,
                errors=[Messages.SERVER_ERROR],
                user=None,
            )


class PasswordReset(PasswordResetBase):
    class Meta:
        description = "Reset the user's password."

    @classmethod
    def perform_mutation(cls, root, info, **kwargs):
        """
        passwordReset(
            token: String!
            newPassword: String!
        ): PasswordReset
        """
        try:
            token = kwargs.get("token")
            password = kwargs.get("newPassword")
            payload = get_token_payload(
                token,
                TokenAction.PASSWORD_RESET,
                settings.EXPIRATION_PASSWORD_RESET_TOKEN,
            )
            user = UserModel._default_manager.get(**payload)
            revoke_user_refresh_token(user)
            # set new password
            user.set_password(password)
            user.save()
            # Token was sent via mail so makes sense to verify
            if user.status.verified is False:
                user.status.verified = True
                user.status.save(update_fields=["verified"])
                user_verified.send(sender=cls, user=user)
            return cls(
                success=True,
                errors=None,
            )
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)
        except Exception as e:
            # notify_admins.apply_async(
            #     args=[
            #         "PasswordReset Mutation Exception",
            #         "Exception details: %s" % str(e),
            #     ],
            #     countdown=10,
            # )
            print("Exception details: %s" % str(e))
            return cls(
                success=False,
                errors=[Messages.SERVER_ERROR],
                user=None,
            )


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()

    #
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()

    #
    register = Register.Field()
    verify_account = VerifyAccount.Field()
    resend_activation_email = ResendActivationEmail.Field()
    send_password_reset_email = SendPasswordResetEmail.Field()
    password_reset = PasswordReset.Field()
