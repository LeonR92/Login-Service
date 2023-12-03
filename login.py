import yaml
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)  # Initialize LoginManager


class User(UserMixin):
    def __init__(self, username, password, role):
        self.id = username
        self.password = password
        self.role = role

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return load_user_from_yaml(user_id)


def load_user_from_yaml(username, yaml_file="config.yaml"):
    with open(yaml_file, "r") as file:
        users = yaml.safe_load(file).get("users", {})
        user_data = users.get(username)
        if user_data:
            return User(username, user_data["password"], user_data["role"])
        return None


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = load_user_from_yaml(username)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin_view"))
            elif user.role == "user":
                return redirect(url_for("user_view"))
        else:
            return "Invalid credentials"
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
def admin_view():
    return render_template("admin.html")


@app.route("/user")
@login_required
def user_view():
    return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)
