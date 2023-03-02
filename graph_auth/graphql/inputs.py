import graphene


class EmailInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="Email")


class RegisterInput(EmailInput):
    username = graphene.String(required=True, description="Username")
    password = graphene.String(required=True, description="Password")


class PasswordResetInput(graphene.InputObjectType):
    token = graphene.String(required=True, description="Token")
    newPassword = graphene.String(required=True, description="NewPassword")
