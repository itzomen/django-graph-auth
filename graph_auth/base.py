import graphene

from .type import ExpectedErrorType

# TODO: if for custom was here
OutputErrorType = ExpectedErrorType


class BaseAuthMutation(graphene.Mutation):
    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(OutputErrorType)

    class Meta:
        abstract = True

    @classmethod
    def mutate(cls, root, info, **data):
        return cls.perform_mutation(root, info, **data)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass

    @classmethod
    def success_response(cls):
        """Return a success response."""
        return cls(**{"errors": []})

    @classmethod
    def unsuccess_response(cls):
        """Return a success response."""
        return cls(**{"errors": ["That did not go Well"]})


class BaseRegister(BaseAuthMutation):

    """
    # how do I pass the arguments to the mutation as it is
    # without defining and input variable so that the mutation
    # can be called like this:
    register(
        email: String!
        username: String!
        password1: String!
        password2: String!
    ): Register
    """

    class Arguments:
        email = graphene.String(required=True, description="Email")
        username = graphene.String(required=True, description="Username")
        password = graphene.String(required=True, description="Password")

    class Meta:
        abstract = True


class VerifyAccountBase(BaseAuthMutation):
    class Arguments:
        token = graphene.String(required=True, description="Token")

    class Meta:
        abstract = True


class ResendActivationEmailBase(BaseAuthMutation):
    class Arguments:
        email = graphene.String(required=True, description="Email")

    class Meta:
        abstract = True


class SendPasswordResetEmailBase(BaseAuthMutation):
    class Arguments:
        email = graphene.String(required=True, description="Email")

    class Meta:
        abstract = True


class PasswordResetBase(BaseAuthMutation):
    class Arguments:
        token = graphene.String(required=True, description="Token")
        newPassword = graphene.String(required=True, description="NewPassword")

    class Meta:
        abstract = True


class PasswordSetBase(BaseAuthMutation):
    class Arguments:
        token = graphene.String(required=True, description="Token")
        newPassword = graphene.String(required=True, description="NewPassword")

    class Meta:
        abstract = True
