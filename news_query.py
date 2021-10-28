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

def get_news(coin):
    Query = discovery.query(
            ENVIRONMENT_ID,
            COLLECTION_ID,
            passages = True, 
            deduplicate= False,
            highlight= True,
        natural_language_query = f'10 most relevant document about {coin}'

    
    )

    return Query.result["results"]

