from flask import session
import validation
import views
import database

def create_review_post(rating: int, comment: str, recipe_id: int, page: int):
    rating = validation.clamp_rating(rating)
    _, comment = validation.limit_lenght(comment, max_len=validation.MAX_MAX_COMMENT_LENGTH)

    database.add_review(session["user_id"], recipe_id, rating, comment)
    return views.show_recipe(recipe_id, page)
