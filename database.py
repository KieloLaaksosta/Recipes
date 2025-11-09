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
        "SELECT PasswordHash FROM Users WHERE username = ?",
        [username], 
    )

def get_user_id(username: str):
    return query(
        "SELECT Id FROM Users WHERE username = ?",
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