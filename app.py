from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema

# Criando a instância do FastAPI
app = FastAPI()

# Adicionando a rota GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

