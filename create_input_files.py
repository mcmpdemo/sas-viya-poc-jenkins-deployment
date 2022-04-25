import sys
import base64
import requests
import urllib.parse as urllib
import yaml
import json

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
    
    SCOPES = "getCertificates getDepAssets getDepAssetsShort getLicense"
    ENDPOINT = "https://api.sas.com/mysas/token"

    payload = "grant_type=client_credentials&client_id={0}&client_secret={1}&scope={2}".format(api_key, api_secret,urllib.quote(SCOPES))
    headers = { 'content-type': "application/x-www-form-urlencoded" }

    response = requests.post(url=ENDPOINT, data=payload, headers=headers)

    return response.json()["access_token"]

def create_id_rsa_file(raw_data):
    private_key_file = open("id_rsa", "w")
    decoded = str(base64.b64decode(raw_data), "utf-8")
    private_key_file.write(decoded)
    private_key_file.close()

def read_fqdn_from_details(order_details):
    return "jp-sas-viya-4-aks-91f5b069.hcp.eastus.azmk8s.io"

def open_ansible_vars_template(filename):
    ansible_vars_template = open(filename, "w")
    data = yaml.load( ansible_vars_template, Loader=yaml.loader.SafeLoader )
    return data, ansible_vars_template

if __name__ == "__main__":

    USER_NAME = sys.argv[1]
    API_KEY = sys.argv[2]
    ORDER_NUMBER = sys.argv[3]
    TENANT_API_URL = sys.argv[4]
    
    TF_STATE_FILE = sys.argv[5]
    ANSIBLE_VARS_TEMPLATE = sys.argv[6]
    
    V4_CFG_SAS_API_KEY = sys.argv[7]
    V4_CFG_SAS_API_SECRET = sys.argv[8]

    V4_CFG_ORDER_NUMBER = sys.argv[9]
    
    ID_RSA = sys.argv[10]

    V4_CFG_CADENCE_VERSION = sys.argv[11]

    print("Getting order details...")
    order_details = get_order_details(USER_NAME, API_KEY, ORDER_NUMBER, TENANT_API_URL)

    print("Creating terraform tf state file...")
    create_terraform_file(TF_STATE_FILE)

    print("Creating ansible vars template file...")
    create_ansible_vars_template(ANSIBLE_VARS_TEMPLATE)

    print("Get sas portal token...")
    token = get_sas_portal_token(V4_CFG_SAS_API_KEY, V4_CFG_SAS_API_SECRET)

    print("Creating id_rsa file...")
    create_id_rsa_file(ID_RSA)

    print("Reading Cluster FQDN...")
    V4_CFG_INGRESS_FQDN = read_fqdn_from_details(order_details)

    print("Render ansible vars template...")

    template_object, ansible_vars_template = open_ansible_vars_template("ansible-vars.yaml")
    template_object["NAMESPACE"]              = NAMESPACE
    template_object["V4_CFG_SAS_API_KEY"]     = V4_CFG_SAS_API_KEY
    template_object["V4_CFG_SAS_API_SECRET"]  = V4_CFG_SAS_API_SECRET
    template_object["V4_CFG_ORDER_NUMBER"]    = V4_CFG_ORDER_NUMBER
    template_object["V4_CFG_INGRESS_FQDN"]    = V4_CFG_INGRESS_FQDN
    template_object["V4_CFG_CADENCE_VERSION"] = V4_CFG_CADENCE_VERSION

    ansible_vars_template.write(yaml.dump(template_object))
    ansible_vars_template.close()

