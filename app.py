from flask import Flask
from flask import render_template, request
import config
import account

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    success_full, error_msg = account.try_create_account(username, password, password_again)
    if not success_full:
        return f"VIRHE: {error_msg}"
    return "Tunnus luotu"