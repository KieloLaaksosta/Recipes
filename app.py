from flask import Flask, render_template, abort, session, request
import config, account, recipes, reviews, views, database

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csfr_token(token):
    session_token = session.get("csfr_token")
    
    if not (session_token and token and token == session_token):
        abort(403)     

def check_login():
    if "username" not in session or "user_id" not in session:
        abort(403)
    if database.get_user_id(session["username"]) != session["user_id"]:
        logout() #username doesn't match what's in database. This indicates session tokens aren't synchronized with database. Logout to force new login. 
        abort(403)

def check_recipe_ownership(recipe_id: int):
    check_login()
    if session["user_id"] != database.get_recipe_owner_id(recipe_id)[0]["Id"]:
        abort(403)

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
    check_login()

    if request.method == "POST":
        check_csfr_token(request.form["csrf_token"])
        return recipes.create_recipe_post(
            request.form["recipe_name"], 
            request.form["ingredients"], 
            request.form["instructions"], 
            request.form.getlist("tags")
        )
    else:
        return recipes.create_recipe_get()

@app.route("/search_recipe", methods=["GET", "POST"])
@app.route("/search_recipe/<int:page>", methods=["POST"])
def search_recipe(page=0):
    if request.method == "POST":
        return recipes.query_recipes_post(request.form["search"], request.form.getlist("tags"), page)
    else:
        return recipes.search_recipe_get()

@app.route("/recipes/<int:recipe_id>", methods=["POST", "GET"])
@app.route("/recipes/<int:recipe_id>/<int:page>", methods=["POST", "GET"])
def show_recipe(recipe_id, page=0):
    if request.method == "POST":
        return reviews.create_review_post(
            int(request.form["rating"]), 
            request.form["comment"], 
            request.form["recipe_id"],
            page
        )
    else:
        return views.show_recipe(recipe_id, page)

@app.route("/users/<int:user_id>", methods=["GET"])
@app.route("/users/<int:user_id>/<int:recipe_page>/<int:review_page>", methods=["GET"])
def show_user(user_id, recipe_page=0, review_page=0):
    return views.show_user(user_id, recipe_page, review_page)

@app.route("/recipes/<int:recipe_id>/edit", methods=["POST", "GET"])
def edit_recipe(recipe_id):
    check_recipe_ownership(recipe_id)
    if request.method == "POST":
        check_csfr_token(request.form["csrf_token"])
        return recipes.edit_recipe_post(
            recipe_id,
            request.form["recipe_name"],
            request.form["instructions"],
            request.form["ingredients"],
            request.form.getlist("tags")
        )
    else:
        return recipes.edit_recipe_get(recipe_id)