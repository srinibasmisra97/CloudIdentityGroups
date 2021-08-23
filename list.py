# Detailed Python Client setup for Cloud Identity APIs can be found here:
# https://cloud.google.com/identity/docs/how-to/setup

from google.oauth2 import service_account
import googleapiclient.discovery
from urllib.parse import urlencode


SCOPES = ['https://www.googleapis.com/auth/cloud-identity.groups']
SERVICE_ACCOUNT_FILE = './identity-groups-admin.json'

CUSTOMER_ID = "C03j0o317"


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
  credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  service_name = 'cloudidentity'
  api_version = 'v1'
  service = googleapiclient.discovery.build(
    service_name,
    api_version,
    credentials=credentials)

  return service


if __name__=="__main__":
    service = create_service()
    print(service)

    search_response = search_google_groups(service=service, customer_id=CUSTOMER_ID)
    print(search_response)