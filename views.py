from flask import render_template
import database

def show_user(user_id: int, recipe_page: int, review_page: int):
    recipes_per_page = 15
    reviews_per_page = 15

    user_info, recipes, reviews = database.get_user_view(
        user_id,
        recipes_per_page * recipe_page,
        recipes_per_page,
        reviews_per_page * review_page,
        reviews_per_page
    )
    if len(user_info) < 1:
        return render_template(
            "not_found.html",
            error_msg="Käyttäjää ei löytynyt."
        )

    return render_template(
        "user.html",
        user_info=user_info[0],
        recipes=recipes,
        reviews=reviews,
        recipe_page=recipe_page,
        review_page=review_page,
        user_id=user_id
    )

def show_recipe(recipe_id: int, page: int):
    reviews_per_page = 15

    recipes, tag_names, reviews = database.get_recipe_and_reviews(recipe_id, reviews_per_page * page, reviews_per_page)
    if len(recipes) < 1:
        return render_template(
            "not_found.html",
            error_msg="Reseptiä ei löytynyt."
        )

    return render_template(
        "recipe.html",
        found=True,
        RecipeId=recipe_id,
        recipe=recipes[0],
        tag_names=tag_names,
        recipe_id=recipe_id,
        reviews=reviews,
        page=page
    )
