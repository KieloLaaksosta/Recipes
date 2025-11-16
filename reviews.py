from flask import redirect, session
import validation, database

def create_review(rating: int, comment: str, recipe_id: int):    
    rating = validation.clamp_rating(rating)
    _, comment = validation.limit_lenght(comment, max=validation.MAX_COMMENT_LENGHT)

    database.add_review(session["user_id"], recipe_id, rating, comment)
    return redirect(f"/recipes/{recipe_id}")