import json

if __name__ == "__main__":
    tf_state_file = open("terraform.tfstate")
    content = tf_state_file.read()
    print(content)
    data = json.load(content)
    print(data)