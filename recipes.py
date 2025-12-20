from flask import  render_template, session, redirect
import database
import validation

def create_recipe_get():
    tags = database.get_available_tags()
    return render_template(
        "create_recipe.html",
        available_tags=tags,
        max_name_len=validation.MAX_RECIPE_NAME_LENGTH,
        max_ingredients_len=validation.MAX_INGREDIENTS_LENGTH,
        max_instructions_len=validation.MAX_INSTRUCTIONS_LENGTH
    )

def create_recipe_post(recipe_name, ingredients, instructions, tag_ids):
    error_code, recipe_name = validation.limit_lenght(
        recipe_name,
        validation.MIN_RECIPE_NAME_LENGTH,
        validation.MAX_RECIPE_NAME_LENGTH
    )
    error_msg = None
    if error_code in [validation.INVALID_TYPE, validation.TOO_SHORT]:
        if error_code == validation.INVALID_TYPE:
            error_msg = "Reseptille tulee antaa nimi."
        if error_code == validation.TOO_SHORT:
            error_msg = f"Reseptin nimen tulee olla vähintään {validation.MIN_RECIPE_NAME_LENGTH} merkkiä pitkä."

    _, ingredients = validation.limit_lenght(ingredients, max_len=validation.MAX_INGREDIENTS_LENGTH)
    _, instructions = validation.limit_lenght(instructions, max_len=validation.MAX_INSTRUCTIONS_LENGTH)

    tag_ids = validation.truncate_list(tag_ids)

    if error_msg:
        tags = database.get_available_tags()
        return render_template(
            "create_recipe.html",
            error_msg=error_msg,
            available_tags=tags,
            name=recipe_name,
            ingredients=ingredients,
            instructions=instructions,
            max_name_len=validation.MAX_RECIPE_NAME_LENGTH,
            max_ingredients_len=validation.MAX_INGREDIENTS_LENGTH,
            max_instructions_len=validation.MAX_INSTRUCTIONS_LENGTH
        )
    database.add_recipe(session["user_id"], recipe_name, ingredients, instructions, tag_ids)
    return redirect("/")

def search_recipe_get():
    tags = database.get_available_tags()
    return render_template(
        "index.html",
        available_tags=tags,
        did_search=False,
        max_search_len=validation.MAX_SEARCH_LENGTH,
        page=0
    )

def search_recipes(orginal_search: str, filter_tag_ids: list, page: int):
    recipes_per_page = 30

    tags = database.get_available_tags()
    
    _, orginal_search = validation.limit_lenght(orginal_search, max_len=validation.MAX_SEARCH_LENGTH)
    filter_tag_ids = validation.truncate_list(filter_tag_ids)
    filter_tag_ids = [int(tag) for tag in filter_tag_ids]

    search = '%'+'%'.join(orginal_search.split(' '))+'%'

    results = database.query_recipes(search, filter_tag_ids, page * recipes_per_page, recipes_per_page)
    return render_template(
        "index.html",
        found_recipes=len(results),
        recipes=results,
        available_tags=tags,
        did_search=True,
        search=orginal_search,
        filter_tag_ids=filter_tag_ids,
        page=page,
        max_search_len=validation.MAX_SEARCH_LENGTH
    )

def edit_recipe_get(recipe_id: int):
    tags = database.get_available_tags()
    recipe, added_tags = database.get_recipe(recipe_id)

    if len(recipe) < 1:
        return render_template(
            "not_found.html",
            error_msg="Reseptiä ei löytynyt."
        )

    return render_template(
        "edit_recipe.html",
        recipe_id=recipe_id,
        available_tags=tags,
        recipe=recipe[0],
        added_tags=list((tag["TagId"] for tag in added_tags)),
        max_name_len=validation.MAX_RECIPE_NAME_LENGTH,
        max_ingredients_len=validation.MAX_INGREDIENTS_LENGTH,
        max_instructions_len=validation.MAX_INSTRUCTIONS_LENGTH,
        max_comment_len=validation.MAX_COMMENT_LENGTH
    )

def edit_recipe_post(
    recipe_id: int,
    recipe_name: str,
    instructions: str,
    ingredients: str,
    added_tags: list
    ):
    error_code, recipe_name = validation.limit_lenght(
        recipe_name,
        validation.MIN_RECIPE_NAME_LENGTH,
        validation.MAX_RECIPE_NAME_LENGTH
    )
    error_msg = None
    if error_code in [validation.INVALID_TYPE, validation.TOO_SHORT]:
        if error_code == validation.INVALID_TYPE:
            error_msg = "Reseptille tulee antaa nimi."
        if error_code == validation.TOO_SHORT:
            error_msg = f"Reseptin nimen tulee olla vähintään {validation.MIN_RECIPE_NAME_LENGTH} merkkiä pitkä."

    _, ingredients = validation.limit_lenght(ingredients, max_len=validation.MAX_INGREDIENTS_LENGTH)
    _, instructions = validation.limit_lenght(instructions, max_len=validation.MAX_INSTRUCTIONS_LENGTH)

    added_tags = validation.truncate_list(added_tags)
    tags = database.get_available_tags()

    recipe = {"Name" : recipe_name, "Instructions": instructions, "Ingredients": ingredients}

    added_tags = [int(tag) for tag in added_tags]

    if not error_msg:
        database.edit_recipe(
            recipe_id,
            recipe_name,
            instructions,
            ingredients,
            added_tags
        )

    return render_template(
        "edit_recipe.html",
        error_msg=error_msg,
        recipe_id=recipe_id,
        available_tags=tags,
        added_tags=added_tags,
        recipe=recipe,
        max_name_len=validation.MAX_RECIPE_NAME_LENGTH,
        max_ingredients_len=validation.MAX_INGREDIENTS_LENGTH,
        max_instructions_len=validation.MAX_INSTRUCTIONS_LENGTH,
        max_comment_len=validation.MAX_COMMENT_LENGTH
    )

def delete(recipe_id: int):
    database.delete_recipe(recipe_id)
    return redirect("/")
