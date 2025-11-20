from flask import  render_template, session, redirect
import database, validation

def create_recipe():
    tags = database.get_available_tags()
    return render_template("create_recipe.html", available_tags=tags)

def add_recipe(recipe_name, ingredients, instructions, tag_names):
    error_code, recipe_name = validation.limit_lenght(recipe_name, validation.MIN_RECIPE_NAME_LENGHT, validation.MAX_RECIPE_NAME_LENGHT)
    if error_code == validation.VALID or error_code == validation.TOO_SHORT: 
        if error_code == validation.INVALID_TYPE:
            error_msg = "Reseptille tulee antaa nimi."
        if error_code == validation.TOO_SHORT:
            error_msg = f"Reseptin nimen tulee olla vähintään {validation.MIN_RECIPE_NAME_LENGHT} merkkiä pitkä."
        return render_template("error_pages/add_recipe.html", error_msg=error_msg)
    
    validation.truncate_list

    _, ingredients = validation.limit_lenght(ingredients, max=validation.MAX_INGREDIENTS_LENGHT)
    _, instructions = validation.limit_lenght(instructions, max=validation.MAX_INSCTRUCTIONS_LENGHT)

    tag_names = validation.truncate_list(tag_names)

    database.add_recipe(session["user_id"], recipe_name, ingredients, instructions, tag_names)
    return redirect("/")

def search_recipe():
    tags = database.get_available_tags()
    return render_template("search_recipe.html", available_tags=tags)

def query_recipes(search: str, tag_ids: list):
    _, search = validation.limit_lenght(search, validation.MAX_SEARCH_LENGHT)
    tag_ids = validation.truncate_list(tag_ids)

    results = database.query_recipes(search, tag_ids)
    return render_template("search_results.html", found_recipes = len(results), recipes=results)