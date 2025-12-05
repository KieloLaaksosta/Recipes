import time
from flask import Flask, abort, session, request, g
import markupsafe
import config
import account
import recipes
import reviews
import views
import database

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def check_csrf_token(token):
    if "csrf_token" not in session:
        abort(403)

    session_token = session["csrf_token"]

    if not (session_token and token and token == session_token):
        abort(403)

def check_login():
    if "user_id" not in session:
        abort(403)

def check_recipe_ownership(recipe_id: int):
    check_login()
    recipe = database.get_recipe_owner_id(recipe_id)
    if len(recipe) < 1:
        abort(404)
    if session["user_id"] != recipe[0]["Id"]:
        abort(403)

def check_review_ownership(review_id: int):
    check_login()
    review = database.get_review_owner_id(review_id)
    if len(review) < 1:
        abort(404)
    if session["user_id"] != review[0]["Id"]:
        abort(403)

@app.route("/", methods=["GET", "POST"])
@app.route("/<int:page>", methods=["GET", "POST"])
def index(page=0):
    if request.method == "POST":
        return recipes.search_recipes(
            request.form["search"],
            request.form.getlist("tags"),
            page
        )
    return recipes.search_recipes("", [], page)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return account.register_post(
            request.form["username"],
            request.form["password"],
            request.form["password_again"],
            request.form["next_page"]
        )

    if request.path != request.referrer:
        next_page_url = request.referrer
    else:
        next_page_url = "/"
    return account.register_get(next_page_url)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return account.login_post(
            request.form["username"],
            request.form["password"],
            request.form["next_page"]
        )

    next_page_url = request.referrer if request.path != request.referrer else "/"
    return account.login_get(next_page_url)

@app.route("/logout")
def logout():
    return account.log_out()

@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    check_login()

    if request.method == "POST":
        check_csrf_token(request.form["csrf_token"])
        return recipes.create_recipe_post(
            request.form["recipe_name"],
            request.form["ingredients"],
            request.form["instructions"],
            request.form.getlist("tags")
        )
    return recipes.create_recipe_get()

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
    return views.show_recipe(recipe_id, page)

@app.route("/users/<int:user_id>", methods=["GET"])
@app.route("/users/<int:user_id>/<int:recipe_page>/<int:review_page>", methods=["GET"])
def show_user(user_id, recipe_page=0, review_page=0):
    return views.show_user(user_id, recipe_page, review_page)

@app.route("/recipes/<int:recipe_id>/edit", methods=["POST", "GET"])
def edit_recipe(recipe_id):
    check_recipe_ownership(recipe_id)
    if request.method == "POST":
        check_csrf_token(request.form["csrf_token"])
        return recipes.edit_recipe_post(
            recipe_id,
            request.form["recipe_name"],
            request.form["instructions"],
            request.form["ingredients"],
            request.form.getlist("tags")
        )
    return recipes.edit_recipe_get(recipe_id)

@app.route("/reviews/<int:review_id>/edit", methods=["POST", "GET"])
def edit_review(review_id):
    check_review_ownership(review_id)
    if request.method == "POST":
        check_csrf_token(request.form["csrf_token"])
        return reviews.edit_review_post(
            review_id,
            request.form["comment"],
            request.form["rating"]
        )
    return reviews.edit_review_get(review_id)

@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id):
    check_recipe_ownership(recipe_id)
    check_csrf_token(request.form["csrf_token"])

    return recipes.delete(recipe_id)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    check_login()
    check_csrf_token(request.form["csrf_token"])
    if session["user_id"] != user_id:
        abort(403)

    return account.delete(
        session["username"],
        user_id,
        request.form["password"],
        request.referrer
    )

@app.route("/reviews/<int:review_id>/delete", methods=["POST"])
def delete_review(review_id):
    check_login()
    check_csrf_token(request.form["csrf_token"])

    return reviews.delete(review_id)
