from flask import render_template, redirect, session
import validation
import views
import database

def create_review_post(rating: int, comment: str, recipe_id: int, page: int):
    rating = validation.clamp_rating(rating)
    _, comment = validation.limit_lenght(comment, max_len=validation.MAX_COMMENT_LENGTH)

    database.add_review(session["user_id"], recipe_id, rating, comment)
    return views.show_recipe(recipe_id, page)

def edit_review_get(review_id: int):
    review = database.get_review(review_id)

    if len(review) < 1:
        return render_template(
            "not_found.html",
            error_msg="Arviota ei löytynyt."
        )

    return render_template(
        "edit_review.html",
        review_id=review_id,
        review=review[0],
        max_comment_len=validation.MAX_COMMENT_LENGTH
    )

def edit_review_post(review_id: int, comment: str, rating: str):
    _, comment = validation.limit_lenght(comment, max_len=validation.MAX_COMMENT_LENGTH)
    rating = validation.clamp_rating(int(rating))

    database.edit_review(
        review_id,
        comment,
        rating,
    )

    return edit_review_get(review_id)


def delete(review_id: int):
    database.delete_review(review_id)
    return redirect("/")
