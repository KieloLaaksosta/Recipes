import sqlite3
from flask import g

def last_insert_id():
    return g.last_insert_id  

def get_connection():
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection

def execute(query: str, params, connection):
    try:
        result = connection.execute(query, params)
        g.last_insert_id = result.lastrowid
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

def query(query: str, params, connection):
    try:
        result = connection.execute(query, params).fetchall()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e

    return result

def get_placeholders(n: int) -> str:
    placeholders = ["?"] * n
    return ", ".join(placeholders)

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
    connection = get_connection()

    try:
        return query(
            "SELECT Id FROM Users WHERE Username = ?",
            [username], 
            connection
        )
    finally:
        connection.close()

def add_recipe(creator, recipe_name: str, ingredients: str, instructions: str, tag_ids: list):
    connection = get_connection()

    try:
        execute(
            """
            INSERT INTO Recipes (Id, Name, CreatorId, Instructions, Ingredients)
            VALUES (NULL, ?, ?, ?, ?)
            """,
            [recipe_name, creator, ingredients, instructions],
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

def get_available_tags():
    connection = get_connection()

    try:
        return query("SELECT Id, Name FROM Tags ORDER BY Id", [], connection)
    finally:
        connection.close()

def query_recipes(search: str, tag_ids: list):
    connection = get_connection()

    try:
        if len(tag_ids) == 0:
            return query(
                """
                SELECT
                    R.Id, R.Name, U.Username AS CreatorName, U.Id AS CreatorId, AVG(Reviews.Rating) AS AverageRating
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
                """,
                [
                    search,
                    search,
                    search
                ],
                connection
            )
        return query(
            f"""
            SELECT
                R.Id, R.Name, U.Username AS CreatorName, U.Id AS CreatorId
            FROM 
                Recipes AS R
                JOIN Users AS U ON U.Id = R.CreatorId
                JOIN TagJoin TJ ON TJ.RecipeId = R.Id
            WHERE 
                (R.Name LIKE ? OR R.Instructions LIKE ? OR R.Ingredients LIKE ?)
                AND TJ.TagId IN ({get_placeholders(len(tag_ids))})
            GROUP BY
                R.Id
            HAVING
                COUNT(DISTINCT TJ.TagId) = ?
            """,
            3 * [search] + tag_ids + [len(tag_ids)],
            connection
        )
    finally:
        connection.close()

def get_recipe(recipe_id : int):
    connection = get_connection()

    try:
        recipe = query(
            """
            SELECT
                R.Id, R.Name, R.Ingredients, R.Instructions, U.Username AS CreatorName, U.Id AS CreatorId
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
                U.Id AS ReviewerId, U.Username AS ReviewerName, R.rating, R.comment
            FROM
                Reviews AS R
                JOIN Users AS U ON R.ReviewerId == U.id
            WHERE
                R.RecipeId = ?
            """,
            [recipe_id],
            connection
        )
        
        tag_names = []
        for row in tags:
            tag_names.append(row["TagName"])
        
        return (recipe, tag_names, reviews)
    finally:
        connection.close()

def get_user_view(user_id : int) -> tuple:
    connection = get_connection()

    try:
        user_info = query(
            """
            SELECT
                U.Username AS Username, COUNT(Recipes.Id) AS RecipeCount, COUNT(Recipes.Id) AS RecipeCount, COUNT(SentReviews.Id) AS ReviewCount, AVG(ReciewedReviews.Rating) AS AverageRating
            FROM 
                Users AS U
                LEFT JOIN Recipes ON Recipes.CreatorId = U.Id 
                LEFT JOIN Reviews AS ReciewedReviews ON ReciewedReviews.RecipeId = Recipes.Id
                LEFT JOIN Reviews AS SentReviews ON SentReviews.ReviewerId = U.Id
            WHERE U.Id = ?
            GROUP BY 
                U.Id;
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
            """,
            [user_id],
            connection
        )

        reviews = query(
            """
            SELECT
                Recipes.Name AS RecipeName, Recipes.Id AS RecipeId, Reviews.Rating AS Rating
            FROM 
                Users AS U
                JOIN Reviews ON Reviews.ReviewerId = U.Id
                JOIN Recipes ON Recipes.Id = Reviews.RecipeId
            WHERE U.Id = ?
            """,
            [user_id],
            connection
        )
    
        for r in recipes:
            print(list(r))

        for r in user_info:
            print(list(r))

        return (user_info, recipes, reviews)
    finally:
        connection.close()

def add_review(reviewer_id: int, recipe_id: int, rating: int, comment: str):
    connection = get_connection()

    try:
        execute(
            "INSERT INTO Reviews (Id, ReviewerId, RecipeId, Rating, Comment) VALUES (NULL, ?, ?, ?, ?)",
            [reviewer_id, recipe_id, rating, comment],
            connection
        )
    finally:
        connection.close()