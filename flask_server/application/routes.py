from flask import current_app as app
from flask_graphql import GraphQLView
import graphene

from application.query import Query
schema = graphene.Schema(query=Query)


@app.route('/')
def index():
    return '<p> Hello World!</p>'


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)
