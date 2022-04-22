import sys
import json
import base64
import requests

NAMESPACE = "viya-4-sas-ns"

def get_order_details(user_name,api_key,order_number,tenant_url):
    
    ENDPOINT = "{0}/v3/api/services/azure/{1}".format(tenant_url, order_number)

    headers = {
        'username': user_name,
        'apikey': api_key
    }   

    response = requests.get(url=ENDPOINT, headers=headers)

    return response.json()

def create_terraform_file(raw_data):
    tf_state_file = open( "terraform.tfstate", "w" )
    decoded = str(base64.b64decode(raw_data), "utf-8")
    tf_state_file.write(decoded)
    tf_state_file.close()

def create_ansible_vars_file(order_details):

    ansible_vars = open("ansible-vars.yaml", "a")

    ansible_vars.write("NAMESPACE: {0}\n\n".format(NAMESPACE))
    ansible_vars.write("DEPLOY: true\n\n")
    ansible_vars.write("V4_CFG_MANAGE_STORAGE: true\n\n")
    ansible_vars.write("V4_CFG_SAS_API_KEY: '{0}'\n\n".format(order_details['v4_cfg_sas_api_key']))

    ansible_vars.close()

if __name__ == "__main__":

    USER_NAME = sys.argv[1]
    API_KEY = sys.argv[2]
    ORDER_NUMBER = sys.argv[3]
    TENANT_API_URL = sys.argv[4]

    order_details = get_order_details(USER_NAME, API_KEY, ORDER_NUMBER, TENANT_API_URL)

    print(order_details)

    '''
    print("Creating terraform tf state file...")
    create_terraform_file(order_details['tf_state_file'])

    print("Creating ansible vars file file...")
    create_ansible_vars_file(order_details)
    '''

