from flask import Flask, render_template, request, redirect, url_for, session
from dashboard import create_dash_app
import bcrypt
import yaml

# Load credentials from the YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

app = Flask(__name__)
app.secret_key = "cL5JBeQpyUqYRVJ4ivpumq02Enk1TJ7CoUxjOPMZgwFklRRRC9e"  # Replace with a random secret key

create_dash_app(app)  # Initialize the Dash app within the Flask app


@app.route("/")
def home():
    return render_template("index.html")  # Assuming your login page is named login.html


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"].encode("utf-8")

    # Retrieve the hashed password from the YAML config
    hashed_password = config["users"].get(username, {}).get("password", "")

    # Debugging: Print the retrieved and encoded values
    print(f"Retrieved hash for {username}: {hashed_password}")
    print(f"Encoded password: {password}")

    if hashed_password:
        hashed_password = hashed_password.encode("utf-8")
        if bcrypt.checkpw(password, hashed_password):
            session["username"] = username  # Store the username in the session
            return redirect("/dash/")
        else:
            return "Invalid credentials, please try again."
    else:
        return "User not found"


@app.route("/logout")
def logout():
    session.pop("username", None)  # Clear the username from the session
    return redirect(url_for("home"))  # Redirect to the home page


if __name__ == "__main__":
    app.run(debug=True)
