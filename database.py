import sqlite3
from flask import g

def last_insert_id():
    return g.last_insert_id  

def get_connection():
    db = sqlite3.connect("database.db")
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row

    return db

def execute(query: str, params):
    db = get_connection()
    try:
        result = db.execute(query, params)
        g.last_insert_id = result.lastrowid
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        raise e

    db.close()

def query(query: str, params):
    db = get_connection()
    try:
        result = db.execute(query, params).fetchall()
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        raise e
    db.close()

    return result

def get_placeholders(n: int) -> str:
    placeholders = ["?"] * n
    return ", ".join(placeholders)

def add_account(username: str, hashed_password):
    execute(
        "INSERT INTO Users (Id, Username, PasswordHash) VALUES (NULL, ?, ?)",
        [username, hashed_password]
    )

def get_password(username: str):
    return query(
        "SELECT PasswordHash FROM Users WHERE Username = ?",
        [username], 
    )

def get_user_id(username: str):
    return query(
        "SELECT Id FROM Users WHERE Username = ?",
        [username], 
    )

def add_recipe(creator, recipe_name: str, ingredients: str, instructions: str, tag_ids: list):
    execute(
        """
        INSERT INTO Recipes (Id, Name, CreatorId, Instructions, Ingredients)
        VALUES (NULL, ?, ?, ?, ?)
        """,
        [recipe_name, creator, ingredients, instructions]
    )

    recipe_id = last_insert_id()
    
    for tag in tag_ids:
        execute(
            """
            INSERT INTO TagJoin (RecipeId, TagId)
            VALUES (?, ?)
            """,
            [recipe_id, tag]
        )

def get_available_tags():
    return query("SELECT Id, Name FROM Tags ORDER BY Id", [])

def query_recipes(search: str, tag_ids: list):
    if len(tag_ids) == 0:
        return query(
            """
            SELECT
                R.Id, R.Name, U.Username As CreatorName, U.Id As CreatorId
            FROM 
                Recipes AS R
                JOIN Users AS U ON U.Id = R.CreatorId
            WHERE 
                (R.Name LIKE ? OR R.Instructions LIKE ? OR R.Ingredients LIKE ?)
            """,
            [
                search,
                search,
                search
            ]
        )
    return query(
        f"""
        SELECT
            R.Id, R.Name, U.Username As CreatorName, U.Id As CreatorId
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
        3 * [search] + tag_ids + [len(tag_ids)]
    )