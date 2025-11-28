from flask import render_template
import database

def show_user(user_id: int):
    user_info, recipes, reviews = database.get_user_view(user_id)
    if len(user_info) < 1:
        return render_template(
            "user.html", 
            found=False
        )
    return render_template(
        "user.html", 
        found=True, 
        user_info=user_info[0], 
        recipes=recipes, 
        reviews=reviews
    )

def show_recipe(recipe_id: int):
    recipes, tag_names, reviews = database.get_recipe_and_reviews(recipe_id)
    print(len(recipes) < 1)
    if len(recipes) < 1:
        return render_template(
            "recipe.html",
            found=False
        )
    return render_template(
        "recipe.html", 
        found=True, 
        RecipeId=recipe_id,
        recipe=recipes[0], 
        tag_names=tag_names, 
        recipe_id=recipe_id, 
        reviews=reviews
    )