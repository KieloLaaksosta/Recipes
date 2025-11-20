from flask import Flask
from flask import render_template, request
import config, account, recipes, reviews, views

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
    return account.create_account(request.form["username"], request.form["password"], request.form["password_again"])

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_account", methods=["POST"])
def login_account():
    return account.login_account(request.form["username"], request.form["password"])
    
@app.route("/logout")
def logout():
    return account.log_out()

@app.route("/create_recipe")
def create_recipe():
    return recipes.create_recipe()

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    return recipes.add_recipe(request.form["recipe_name"], request.form["ingredients"], request.form["instructions"], request.form.getlist("tags"))

@app.route("/search_recipe", methods=["GET", "POST"])
def search_recipe():
    if request.method == "POST":
        return recipes.query_recipes_post(request.form["search"], request.form.getlist("tags"))
    else:
        return recipes.search_recipe_get()

@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def show_recipe(recipe_id):
    return views.show_recipe(recipe_id)

@app.route("/users/<int:user_id>", methods=["GET"])
def show_user(user_id):
    return views.show_user(user_id)

@app.route("/create_review", methods=["POST"])
def create_review():
    return reviews.create_review(int(request.form["rating"]), request.form["comment"], request.form["recipe_id"])