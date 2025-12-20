import sqlite3
from flask import g

def get_connection():
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection

def get_placeholders(n: int) -> str:
    placeholders = ["?"] * n
    return ", ".join(placeholders)

def last_insert_id():
    return g.last_insert_id

def execute(sql: str, params, connection):
    try:
        result = connection.execute(sql, params)
        g.last_insert_id = result.lastrowid
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def query(sql: str, params, connection):
    try:
        result = connection.execute(sql, params).fetchall()
    except Exception as e:
        connection.rollback()
        raise e

    return result

#######
#Users#
#######

def add_account(username: str, hashed_password):
    connection = get_connection()

    try:
        execute(
            "INSERT INTO Users (Id, Username, PasswordHash) VALUES (NULL, ?, ?)",
            [username, hashed_password],
            connection
        )
    finally:
        connection.close()

def get_password(username: str):
    connection = get_connection()

    try:
        return query(
            "SELECT PasswordHash FROM Users WHERE Username = ?",
            [username],
            connection
        )
    finally:
        connection.close()

def get_user_id(username: str):
    """Retrieves the Id for a given username."""
    connection = get_connection()

    try:
        return query(
            "SELECT Id FROM Users WHERE Username = ?",
            [username],
            connection
        )
    finally:
        connection.close()

def get_user_view(
        user_id: int,
        recipe_offset: int,
        recipe_limit: int,
        review_offset: int,
        review_limit: int
    ) -> tuple:
    connection = get_connection()

    try:
        user_info = query(
            """
            SELECT
                U.Username AS Username,
                U.Id AS UserId,
                COALESCE(R.RecipeCount, 0) AS RecipeCount,
                COALESCE(SR.ReviewCount, 0) AS ReviewCount,
                RR.AverageRating
            FROM
                Users AS U
            LEFT JOIN (
                SELECT
                    CreatorId,
                    COUNT(Id) AS RecipeCount
                FROM
                    Recipes
                GROUP BY
                    CreatorId
            ) AS R ON R.CreatorId = U.Id
            LEFT JOIN (
                SELECT
                    ReviewerId,
                    COUNT(Id) AS ReviewCount
                FROM
                    Reviews
                GROUP BY
                    ReviewerId
            ) AS SR ON SR.ReviewerId = U.Id
            LEFT JOIN (
                SELECT
                    Recipes.CreatorId,
                    AVG(Reviews.Rating) AS AverageRating
                FROM
                    Recipes
                    JOIN Reviews ON Reviews.RecipeId = Recipes.Id
                GROUP BY
                    Recipes.CreatorId
            ) AS RR ON RR.CreatorId = U.Id
            WHERE U.Id = ?;
            """,
            [user_id],
            connection
        )

        recipes = query(
            """
            SELECT
                R.Name AS RecipeName, R.Id AS RecipeId
            FROM
                Users AS U
                JOIN Recipes AS R ON R.CreatorId = U.Id
            WHERE U.Id = ?
            LIMIT
                ?
            OFFSET
                ?
            """,
            [user_id, recipe_limit, recipe_offset],
            connection
        )

        reviews = query(
            """
            SELECT
                Reviews.Id AS ID, Recipes.Name AS RecipeName, Recipes.Id AS RecipeId, Reviews.Rating AS Rating
            FROM
                Users AS U
                JOIN Reviews ON Reviews.ReviewerId = U.Id
                JOIN Recipes ON Recipes.Id = Reviews.RecipeId
            WHERE U.Id = ?
            LIMIT
                ?
            OFFSET
                ?
            """,
            [user_id, review_limit, review_offset],
            connection
        )

        return (user_info, recipes, reviews)
    finally:
        connection.close()

def delete_user(user_id: int):
    """Deletes a user account."""
    connection = get_connection()

    try:
        return execute(
            "DELETE FROM Users WHERE Id = ?;",
            [user_id],
            connection
        )
    finally:
        connection.close()

#########
#Recipes#
#########

def add_recipe(creator, recipe_name: str, ingredients: str, instructions: str, tag_ids: list):
    connection = get_connection()

    try:
        execute(
            """
            INSERT INTO Recipes (Id, Name, CreatorId, Instructions, Ingredients)
            VALUES (NULL, ?, ?, ?, ?)
            """,
            [recipe_name, creator, instructions, ingredients],
            connection
        )

        recipe_id = last_insert_id()

        for tag in tag_ids:
            execute(
                """
                INSERT INTO TagJoin (RecipeId, TagId)
                VALUES (?, ?)
                """,
                [recipe_id, tag],
                connection
            )
    finally:
        connection.close()

def query_recipes(search: str, tag_ids: list, offset: int, limit: int):
    connection = get_connection()

    try:
        search_pattern = f"%{search}%"
        if len(tag_ids) == 0:
            return query(
                """
                SELECT
                    R.Id AS Id, R.Name AS Name, U.Username AS CreatorName, U.Id AS CreatorId, AVG(Reviews.Rating) AS AverageRating
                FROM
                    Recipes AS R
                    JOIN Users AS U ON U.Id = R.CreatorId
                    LEFT JOIN Reviews ON Reviews.RecipeId = R.Id
                WHERE
                    (R.Name LIKE ? OR R.Instructions LIKE ? OR R.Ingredients LIKE ?)
                GROUP BY
                    R.Id
                ORDER BY
                    AverageRating
                LIMIT
                    ?
                OFFSET
                    ?
                """,
                [
                    search_pattern,
                    search_pattern,
                    search_pattern,
                    limit,
                    offset
                ],
                connection
            )

        return query(
            f"""
            SELECT
                R.Id, R.Name, U.Username AS CreatorName, U.Id AS CreatorId, AVG(Reviews.Rating) AS AverageRating
            FROM
                Recipes AS R
                JOIN Users AS U ON U.Id = R.CreatorId
                JOIN TagJoin TJ ON TJ.RecipeId = R.Id
                LEFT JOIN Reviews ON Reviews.RecipeId = R.Id
            WHERE
                (R.Name LIKE ? OR R.Instructions LIKE ? OR R.Ingredients LIKE ?)
                AND TJ.TagId IN ({get_placeholders(len(tag_ids))})
            GROUP BY
                R.Id
            HAVING
                COUNT(DISTINCT TJ.TagId) = ?
            """,
            [search_pattern, search_pattern, search_pattern] + tag_ids + [len(tag_ids)],
            connection
        )
    finally:
        connection.close()

def get_recipe(recipe_id: int):
    connection = get_connection()
    try:
        recipe = query(
            """
            SELECT
                R.Name, R.Ingredients, R.Instructions, U.Username AS CreatorName, U.Id AS CreatorId
            FROM
                Recipes AS R
                JOIN Users AS U ON U.Id = R.CreatorId
            WHERE
                R.Id = ?
            """,
            [recipe_id],
            connection
        )

        tags = query(
            """
            SELECT
                T.Id AS TagId
            FROM
                Tags AS T
                JOIN TagJoin AS TJ ON T.Id = TJ.TagId
            WHERE
                TJ.RecipeId = ?
            """,
            [recipe_id],
            connection
        )

        return recipe, tags
    finally:
        connection.close()

def get_recipe_and_reviews(recipe_id: int, offset: int, limit: int):
    connection = get_connection()

    try:
        recipe = query(
            """
            SELECT
                R.Name AS Name, R.Ingredients AS Ingredients, R.Instructions AS Instructions, U.Username AS CreatorName, U.Id AS CreatorId
            FROM
                Recipes AS R
                JOIN Users AS U ON U.Id = R.CreatorId
            WHERE
                R.Id = ?
            """,
            [recipe_id],
            connection
        )

        tags = query(
            """
            SELECT
                T.Name AS TagName
            FROM
                Tags AS T
                JOIN TagJoin AS TJ ON T.Id = TJ.TagId
            WHERE
                TJ.RecipeId = ?
            """,
            [recipe_id],
            connection
        )

        reviews = query(
            """
            SELECT
                R.Id AS Id, U.Id AS ReviewerId, U.Username AS ReviewerName, R.rating, R.comment
            FROM
                Reviews AS R
                JOIN Users AS U ON R.ReviewerId == U.id
            WHERE
                R.RecipeId = ?
            LIMIT
                ?
            OFFSET
                ?
            """,
            [recipe_id, limit, offset],
            connection
        )

        print(list((tag["TagName"] for tag in tags)) if len(tags) > 0 else None)

        return recipe, [tag["TagName"] for tag in tags] if len(tags) > 0 else None, reviews
    finally:
        connection.close()

def edit_recipe(recipe_id: int, recipe_name: str, instructions: str, ingredients: str, tags: list):
    connection = get_connection()

    try:
        execute(
            "UPDATE Recipes SET Name = ?, Instructions = ?, Ingredients = ? WHERE Id = ?",
            [recipe_name, instructions, ingredients, recipe_id],
            connection
        )
        #Remove previous tags
        execute(
            "DELETE FROM TagJoin WHERE RecipeId = ?",
            [recipe_id],
            connection
        )
        #Add new tags
        for tag_id in tags:
            execute(
                """
                INSERT INTO TagJoin (RecipeId, TagId)
                VALUES (?, ?)
                """,
                [recipe_id, tag_id],
                connection
            )
    finally:
        connection.close()

def get_recipe_owner_id(recipe_id: int):
    connection = get_connection()

    try:
        return query(
            """
            SELECT
                CreatorId AS Id
            FROM
                Recipes
            WHERE
                Id = ?
            """,
            [recipe_id],
            connection
        )
    finally:
        connection.close()

def delete_recipe(recipe_id: int):
    """Deletes a recipe."""
    connection = get_connection()

    try:
        return execute(
            "DELETE FROM Recipes WHERE Id = ?;",
            [recipe_id],
            connection
        )
    finally:
        connection.close()

#########
#REVIEWS#
#########

def add_review(reviewer_id: int, recipe_id: int, rating: int, comment: str):
    """Inserts a new review for a recipe."""
    connection = get_connection()

    try:
        execute(
            "INSERT INTO Reviews (Id, ReviewerId, RecipeId, Rating, Comment) VALUES (NULL, ?, ?, ?, ?)",
            [reviewer_id, recipe_id, rating, comment],
            connection
        )
    finally:
        connection.close()

def get_review(review_id):
    connection = get_connection()

    try:
        return query(
            "SELECT Comment, Rating FROM Reviews WHERE Id = ?",
            [review_id],
            connection
        )
    finally:
        connection.close()

def edit_review(review_id: int, comment: str, rating: int):
    connection = get_connection()

    try:
        execute(
            "UPDATE Reviews SET Comment = ?, Rating = ? WHERE Id = ?",
            [comment, rating, review_id],
            connection
        )
    finally:
        connection.close()

def get_review_owner_id(review_id: int):
    connection = get_connection()

    try:
        return query(
            """
            SELECT
                ReviewerId AS Id
            FROM
                Reviews
            WHERE
                Id = ?
            """,
            [review_id],
            connection
        )
    finally:
        connection.close()

######
#Tags#
######

def get_available_tags():
    """Retrieves all available tags."""
    connection = get_connection()

    try:
        return query("SELECT Id, Name FROM Tags ORDER BY Id", [], connection)
    finally:
        connection.close()

def delete_review(review_id: int):
    connection = get_connection()

    try:
        return execute(
            "DELETE FROM Reviews WHERE Id = ?;",
            [review_id],
            connection
        )
    finally:
        connection.close()
