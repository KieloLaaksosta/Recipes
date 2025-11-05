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