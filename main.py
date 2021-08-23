# Detailed Python Client setup for Cloud Identity APIs can be found here:
# https://cloud.google.com/identity/docs/how-to/setup

import os
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
from urllib.parse import urlencode
from flask import jsonify


CUSTOMER_ID = os.environ.get("CUSTOMER_ID")
FILTER_STRING = os.environ.get("FILTER_STRING")

credentials = GoogleCredentials.get_application_default()


def search_google_groups(service, customer_id):
  search_query = urlencode({
          "query": "parent=='customerId/{}' && 'cloudidentity.googleapis.com/groups.discussion_forum' in labels".format(customer_id)
  })
  search_group_request = service.groups().search()
  param = "&" + search_query
  search_group_request.uri += param
  response = search_group_request.execute()

  return response

def create_service():
  service_name = 'cloudidentity'
  api_version = 'v1'
  service = googleapiclient.discovery.build(
    service_name,
    api_version,
    credentials=credentials)

  return service


def filter(filterString, groupsResponse):
    groups = []
    group = {
        "id": "",
        "email": "",
        "name": ""
    }
    for g in groupsResponse:
        if g['groupKey']['id'].startswith(filterString):
            group['id'] = g['name']
            group['email'] = g['groupKey']['id']
            group['name'] = g['displayName']
            groups.append(group)
    return(groups)


def list(request):
    if request.method != "GET":
        return jsonify({
            'success': False,
            'message': 'method not allowed'
        }), 405
    
    service = create_service()
    search_response = search_google_groups(service=service, customer_id=CUSTOMER_ID)
    groups = filter(FILTER_STRING, search_response['groups'])
    return jsonify({
        'groups': groups,
        'success': True
    })
