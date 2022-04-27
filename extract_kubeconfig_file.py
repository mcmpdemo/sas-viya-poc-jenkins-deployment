import json

if __name__ == "__main__":
    
    tf_state_file = open("terraform.tfstate")
    content = tf_state_file.read()
    tf_state_file.close()
    data = json.loads(content)
    
    kube_config_data = data["outputs"]["kube_config"]["value"]
    kube_config_file = open("kubeconfig","w")
    kube_config_file.write(kube_config_data)
    kube_config_file.close()