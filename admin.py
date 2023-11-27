import bcrypt
import yaml
import os
import argparse


def add_user_to_yaml(username, password, yaml_file="config.yaml"):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    if os.path.exists(yaml_file):
        with open(yaml_file, "r") as file:
            users = yaml.safe_load(file) or {"users": {}}
    else:
        users = {"users": {}}

    users["users"][username] = {"password": hashed_password.decode("utf-8")}

    with open(yaml_file, "w") as file:
        yaml.dump(users, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a user to YAML file.")
    parser.add_argument("username", type=str, help="Username to add")
    parser.add_argument("password", type=str, help="Password for the user")
    parser.add_argument(
        "--file",
        type=str,
        default="config.yaml",
        help="YAML file to use (default: config.yaml)",
    )

    args = parser.parse_args()
    add_user_to_yaml(args.username, args.password, args.file)

# Run admin.py new_username new_password to create a newuser
