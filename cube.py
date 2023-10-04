from cube import config, file_repository
import json
import os

config.base_path = '/cube-api'

config.schema_path = 'models'

config.telemetry = False

# Access Control

@config('query_rewrite')
def query_rewrite(query: dict, ctx: dict) -> dict:
  if 'user_id' in ctx['securityContext']:
    query['filters'].append({
      'member': 'orders_view.users_id',
      'operator': 'equals',
      'values': [ctx['securityContext']['user_id']]
    })
  return query

# Dynamic Data Model

@config('context_to_app_id')
def context_mapping(ctx: dict):
  return ctx['securityContext'].setdefault('team')

@config('check_sql_auth')
def check_sql_auth(query: dict, username: str) -> dict:
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

@config('semantic_layer_sync')
def sls(ctx: dict) -> list:
   return [{
      'type': 'preset',
      'name': 'Preset Sync',
      'config': {
        'database': 'Cube Cloud: cube_demo',
        'api_token': os.environ['PRESET_API_TOKEN'],
        'api_secret': os.environ['PRESET_API_SECRET'],
        'workspace_url': os.environ['PRESET_WORKSPACE_URL']
      }
    }, {
      'type': "tableau",
      'name': "Tableau Sync",
      'config': {
        'database': "Cube Cloud: cube_demo",
        'region': "10ax",
        'site': "cubedevartyom",
        'personalAccessToken': "demo-cube-cloud",
        'personalAccessTokenSecret': os.environ['TABLEAU_PAT_SECRET']
      }
    }, {
      'type': "metabase",
      'name': "Metabase Sync",
      'config': {
        'database': "Cube Cloud: cube_demo",
        'user': os.environ['METABASE_SLS_USER'],
        'password': os.environ['METABASE_SLS_PASSWORD'],
        'url': os.environ['METABASE_SLS_URL']
      }
    }];

@config('repository_factory')
def repository_factory(ctx: dict) -> list[dict]:
  return file_repository('models')

@config('logger')
def logger(message: str, params: dict) -> None:
  print(f'MY CUSTOM LOGGER --> {message}: {params}')

@config('context_to_api_scopes')
def context_to_api_scopes(context: dict, default_scopes: list[str]) -> list[str]:
  return ['meta', 'data', 'graphql']