import json

if __name__ == "__main__":
    tf_state_file = open("terraform.tfstate")
    content = tf_state_file.read()
    data = json.loads(content)
    print(data)