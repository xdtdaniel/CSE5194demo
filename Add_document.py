import json,os
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from variable import VERSION, URL, API_KEY,COLLECTION_ID, ENVIRONMENT_ID
authenticator = IAMAuthenticator(API_KEY)
discovery = DiscoveryV1(
    version=VERSION,
    authenticator=authenticator
)

discovery.set_service_url(URL)

#add documents
def add_documents(file_path = '', file_name = ''):
   with open(os.path.join(os.getcwd(), file_path, file_name)) as fileinfo:
    add_doc = discovery.add_document(ENVIRONMENT_ID, COLLECTION_ID, file=fileinfo).get_result()
    print(json.dumps(add_doc, indent=2)) 
add_documents('','articles.json')
# def add_documents_from_remote(file_stream):
#     add_doc = discovery.add_document(ENVIRONMENT_ID, COLLECTION_ID, file=file_stream).get_result()
#     print(json.dumps(add_doc, indent=2))