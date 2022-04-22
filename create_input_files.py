import sys
import base64
import requests
import yaml
import json
import http.client

NAMESPACE = "viya-4-sas-ns"

def get_order_details(user_name,api_key,order_number,tenant_url):
    ENDPOINT = "{0}/v3/api/services/azure/{1}".format(tenant_url, order_number)
    headers = { 'username': user_name, 'apikey': api_key}   
    response = requests.get(url=ENDPOINT, headers=headers)
    return response.json()

def create_terraform_file(raw_data):
    tf_state_file = open( "terraform.tfstate", "w" )
    decoded = str(base64.b64decode(raw_data), "utf-8")
    tf_state_file.write(decoded)
    tf_state_file.close()

def create_ansible_vars_template(raw_data):
    ansible_vars_file = open("ansible-vars.yaml", "w")
    decoded = str(base64.b64decode(raw_data), "utf-8")
    ansible_vars_file.write(decoded)
    ansible_vars_file.close()

def get_sas_portal_token(api_key,api_secret):
    
    SCOPES = "getCertificates+getDepAssets+getDepAssetsShort+getLicense"
    ENDPOINT = "https://api.sas.com/mysas/token"

    conn = http.client.HTTPSConnection("")
    payload = "grant_type=client_credentials&client_id={0}&client_secret={1}&scope={2}".format(api_key, api_secret,SCOPES)
    headers = { 'content-type': "application/x-www-form-urlencoded" }

    conn.request("POST", ENDPOINT, payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


if __name__ == "__main__":

    USER_NAME = sys.argv[1]
    API_KEY = sys.argv[2]
    ORDER_NUMBER = sys.argv[3]
    TENANT_API_URL = sys.argv[4]
    
    TF_STATE_FILE = sys.argv[5]
    ANSIBLE_VARS_TEMPLATE = sys.argv[6]
    
    V4_CFG_SAS_API_KEY = sys.argv[7]
    V4_CFG_SAS_API_SECRET = sys.argv[8]

    print("Getting order details...")
    order_details = get_order_details(USER_NAME, API_KEY, ORDER_NUMBER, TENANT_API_URL)

    print("Creating terraform tf state file...")
    create_terraform_file(TF_STATE_FILE)

    print("Creating ansible vars template file...")
    create_ansible_vars_template(ANSIBLE_VARS_TEMPLATE)

    print("Get sas portal token...")
    get_sas_portal_token(V4_CFG_SAS_API_KEY, V4_CFG_SAS_API_SECRET)

