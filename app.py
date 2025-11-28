from flask import Flask, render_template, request
import config, account, recipes, reviews, views

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return account.register_post(
            request.form["username"], 
            request.form["password"], 
            request.form["password_again"]
        )
    else:
        return account.register_get()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return account.login_post(
            request.form["username"], 
            request.form["password"]
        )
    else:
        return account.login_get()
    
@app.route("/logout")
def logout():
    return account.log_out()

@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    if request.method == "POST":
        return recipes.create_recipe_post(
            request.form["recipe_name"], 
            request.form["ingredients"], 
            request.form["instructions"], 
            request.form.getlist("tags")
        )
    else:
        return recipes.create_recipe_get()

@app.route("/search_recipe", methods=["GET", "POST"])
def search_recipe():
    if request.method == "POST":
        return recipes.query_recipes_post(request.form["search"], request.form.getlist("tags"))
    else:
        return recipes.search_recipe_get()

@app.route("/recipes/<int:recipe_id>", methods=["POST", "GET"])
def show_recipe(recipe_id):
    if request.method == "POST":
        return reviews.create_review_post(
            int(request.form["rating"]), 
            request.form["comment"], 
            request.form["recipe_id"]
        )
    else:
        return views.show_recipe(recipe_id)

@app.route("/users/<int:user_id>", methods=["GET"])
def show_user(user_id):
    return views.show_user(user_id)

@app.route("/recipes/<int:recipe_id>/edit", methods=["POST", "GET"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        return recipes.edit_recipe_post(
            recipe_id,
            request.form["recipe_name"],
            request.form["instructions"],
            request.form["ingredients"],
            request.form.getlist("tags")
        )
    else:
        return recipes.edit_recipe_get(recipe_id)