import json,os
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from variable import VERSION, URL, API_KEY,COLLECTION_ID, ENVIRONMENT_ID

def get_discovery_instance():
    authenticator = IAMAuthenticator(API_KEY)
    discovery = DiscoveryV1(
        version=VERSION,
        authenticator=authenticator
    )
    discovery.set_service_url(URL)
    
    return discovery
    
def run_query(discovery, coin_name, query):
    Query = discovery.query(
            ENVIRONMENT_ID,
            COLLECTION_ID,
            aggregation = f"filter(enriched_text.entities.text:{coin_name}).term(enriched_text.sentiment.document.label,count:{query})"
    )
    
    return Query