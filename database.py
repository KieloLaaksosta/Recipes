import sqlite3
from flask import g

def last_insert_id():
    return g.last_insert_id  

def query(query: str, params):
    db = sqlite3.connect("database.db")
    try:
        result = db.execute(query, params).fetchall()
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        raise e
    db.close()

    return result

def execute(command: str, params):
    db = sqlite3.connect("database.db")
    try:
        result = db.execute(command, params)
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        raise e
    g.last_insert_id = result.lastrowid
    db.close()

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

def add_recipe(creator, recipe_name: str, ingredients: str, instructions: str, tags: list):
    execute(
        """
        INSERT INTO Recipes (Id, Name, CreatorId, Instructions, Ingredients)
        VALUES (NULL, ?, ?, ?, ?)
        """,
        [recipe_name, creator, ingredients, instructions]
    )
    
    for tag in tags:
        execute(
            """
            INSERT INTO TagJoin (RecipeId, TagId)
            VALUES (?, ?)
            """,
            [last_insert_id(), tag]
        )

def get_available_tags():
    return query("SELECT Id, Name FROM Tags ORDER BY Id", [])