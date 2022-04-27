import json

if __name__ == "__main__":
    tf_state_file = open("terraform.tfstate")

    data = json.load(tf_state_file.read())

    print(data)