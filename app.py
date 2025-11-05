from flask import Flask
from flask import render_template, request, session, redirect
import config, database, account

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    success_full, error_msg = account.try_create_account(username, password, password_again)
    if not success_full:
        return f"VIRHE: {error_msg}" + '   <a href="/register">yritä uudestaan</a>   <a href="/">palaa alkuun</a>'
    
    session["username"] = username
    session["user_id"] = database.get_user_id(username)
    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_account", methods=["POST"])
def login_account():
    username = request.form["username"]
    password = request.form["password"]

    if account.check_password(username, password):
        session["username"] = username
        return redirect("/")
    else:
        return 'Väärä käyttäjätunnus tai salasana   <a href="/register">yritä uudestaan</a>   <a href="/">palaa alkuun</a>'
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")