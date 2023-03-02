from graph_auth.schema import AuthMutation, AuthQuery
import graphene

class Query(
    AuthQuery,
    graphene.ObjectType,
):
    pass


class Mutation(
    AuthMutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

