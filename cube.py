from cube import config, file_repository
import json
import os

config.base_path = '/cube-api'

config.schema_path = 'models'

config.telemetry = False

# Access Control

# Fix query_rewrite compatibility with SQL push down

# @config('query_rewrite')
# def query_rewrite(query: dict, ctx: dict) -> dict:
#   if 'user_id' in ctx['securityContext']:
#     query['filters'].append({
#       'member': 'orders_view.users_id',
#       'operator': 'equals',
#       'values': [ctx['securityContext']['user_id']]
#     })
#   return query

# Dynamic Data Model

@config('context_to_app_id')
def context_mapping(ctx: dict):
  return ctx['securityContext'].setdefault('team')

@config('check_sql_auth')
def check_sql_auth(query: dict, username: str, password: str) -> dict:
  security_context = {
    'team': username
  }

  return {
    'password': os.environ['CUBEJS_SQL_PASSWORD'],
    'securityContext': security_context
  }

# @config('driver_factory')
# def driver_factory(ctx: dict) -> None:
#   context = ctx['securityContext']
#   data_source = ctx['dataSource']
 
#   if data_source == 'postgres':
#     return {
#       'type': 'postgres',
#       'host': 'demo-db-examples.cube.dev',
#       'user': 'cube',
#       'password': '12345',
#       'database': 'ecom'
#     }


# contextToOrchestratorId
# canSwitchUser


# Custom check auth. TODO: not sure it is working
#
# @config('check_auth')
# def check_auth(ctx: dict, token: str) -> None:
#   if token == 'my_secret_token':
#     ctx['securityContext'] = {}
#     return 

#   raise Exception('Access denied')

@config('repository_factory')
def repository_factory(ctx: dict) -> list[dict]:
  return file_repository('models')

@config('logger')
def logger(message: str, params: dict) -> None:
  print(f'MY CUSTOM LOGGER --> {message}: {params}')

@config('context_to_api_scopes')
def context_to_api_scopes(context: dict, default_scopes: list[str]) -> list[str]:
  return ['meta', 'data', 'graphql']

@config('semantic_layer_sync')
def sls(ctx: dict) -> list:
    return [{
  "type": "tableau-cloud",
  "name": "Cube Dev Tableau Cloud Sync",
  "config": {
    "database": "Cube Cloud: treadwell_cube_demo",
    "region": "us-west-2b",
    "site": "cubedev",
    "personalAccessToken": "treadwell_cube_demo",
    "personalAccessTokenSecret": os.environ['CUBEJS_TABLEAU_PAT_SECRET']
  }
}]