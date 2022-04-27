import os
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
    return "20.232.80.158"

def open_ansible_vars_template(filename):
    ansible_vars_template = open(filename)
    data = yaml.load( ansible_vars_template, Loader=yaml.loader.SafeLoader )
    ansible_vars_template.close()
    return data

if __name__ == "__main__":

    USER_NAME = os.getenv("USER_NAME")
    API_KEY = os.getenv("API_KEY")
    ORDER_NUMBER = os.getenv("ORDER_NUMBER")
    TENANT_API_URL = os.getenv("TENANT_API_URL")
    
    #TF_STATE_FILE = ""
    ANSIBLE_VARS_TEMPLATE = os.getenv("ANSIBLE_VARS_TEMPLATE")
    
    V4_CFG_SAS_API_KEY = os.getenv("V4_CFG_SAS_API_KEY")
    V4_CFG_SAS_API_SECRET = os.getenv("V4_CFG_SAS_API_SECRET")

    V4_CFG_ORDER_NUMBER = os.getenv("V4_CFG_ORDER_NUMBER")
    
    ID_RSA = os.getenv("ID_RSA")

    V4_CFG_CADENCE_VERSION = os.getenv("V4_CFG_CADENCE_VERSION")

    print("Getting order details...")
    order_details = get_order_details(USER_NAME, API_KEY, ORDER_NUMBER, TENANT_API_URL)

    #print("Creating terraform tf state file...")
    #create_terraform_file(TF_STATE_FILE)

    print("Creating ansible vars template file...")
    create_ansible_vars_template(ANSIBLE_VARS_TEMPLATE)

    print("Get sas portal token...")
    token = get_sas_portal_token(V4_CFG_SAS_API_KEY, V4_CFG_SAS_API_SECRET)

    print("Creating id_rsa file...")
    create_id_rsa_file(ID_RSA)

    print("Reading Cluster FQDN...")
    V4_CFG_INGRESS_FQDN = read_fqdn_from_details(order_details)

    print("Render ansible vars template...")

    template_object = open_ansible_vars_template("ansible-vars.yaml")
    template_object["NAMESPACE"]              = NAMESPACE
    template_object["V4_CFG_SAS_API_KEY"]     = V4_CFG_SAS_API_KEY
    template_object["V4_CFG_SAS_API_SECRET"]  = V4_CFG_SAS_API_SECRET
    template_object["V4_CFG_ORDER_NUMBER"]    = V4_CFG_ORDER_NUMBER
    template_object["V4_CFG_INGRESS_FQDN"]    = V4_CFG_INGRESS_FQDN
    template_object["V4_CFG_CADENCE_VERSION"] = V4_CFG_CADENCE_VERSION

    ansible_vars_template = open("ansible-vars.yaml", "w")   
    ansible_vars_template.write(yaml.dump(template_object))
    ansible_vars_template.close()

