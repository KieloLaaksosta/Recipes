from flask import render_template
import database

def show_user(user_id: int):
    user_info, recipes, reviews = database.get_user_view(user_id)
    if(len(user_info) < 1):
        return render_template("error_pages/user_not_found.html")
    return render_template("user.html", user_info=user_info[0], recipes=recipes, reviews=reviews)

def show_recipe(recipe_id: int):
    recipes, tag_names, reviews = database.get_recipe(recipe_id)
    if(len(recipes) < 1):
        return "Reseptiä ei löytynyt."
    return render_template("recipe.html", recipe=recipes[0], tag_names=tag_names, recipe_id=recipe_id, reviews=reviews)