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
    session["user_id"] = database.get_user_id(username)[0]["Id"]
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
        session["user_id"] = database.get_user_id(username)[0]["Id"]
        return redirect("/")
    else:
        return 'Väärä käyttäjätunnus tai salasana   <a href="/login">yritä uudestaan</a>   <a href="/">palaa alkuun</a>'
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_recipe")
def create_recipe():
    tags = database.get_available_tags()
    return render_template("create_recipe.html", available_tags=tags)

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    recipe_name = request.form["recipe_name"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]

    tag_names = request.form.getlist("tags")

    database.add_recipe(session["user_id"], recipe_name, ingredients, instructions, tag_names)
    return redirect("/")

@app.route("/search_recipe")
def search_recipe():
    tags = database.get_available_tags()
    return render_template("search_recipe.html", available_tags=tags)

@app.route("/query_recipes", methods=["POST"])
def query_recipes():
    search = request.form["search"]
    tag_names = request.form.getlist("tags")

    results = database.query_recipes(search, tag_names)
    return render_template("search_results.html", found_recipes = len(results), recipes=results)

@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def show_recipe(recipe_id):
    recipes, tag_names, reviews = database.get_recipe(recipe_id)
    if(len(recipes) < 1):
        return "Reseptiä ei löytynyt."
    return render_template("recipe.html", recipe=recipes[0], tag_names=tag_names, recipe_id=recipe_id, reviews=reviews)

@app.route("/users/<int:user_id>", methods=["GET"])
def show_user(user_id):
    user_info, recipes, reviews = database.get_user_view(user_id)
    if(len(user_info) < 1):
        return "Käyttäjää ei löytynyt."
    return render_template("user.html", user_info=user_info[0], recipes=recipes, reviews=reviews)

@app.route("/create_review", methods=["POST"])
def create_review():
    rating = int(request.form["rating"])
    comment = request.form["comment"]
    recipe_id = request.form["recipe_id"]

    database.add_review(session["user_id"], recipe_id, rating, comment)
    return redirect(f"/recipes/{recipe_id}")