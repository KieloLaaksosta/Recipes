import sqlite3

CONSTRAIN_FAILED = 1
OTHER = 0

def query(command: str, *params):
    db = sqlite3.connect("database.db")
    try:
        result = db.execute(command, [*params]).fetchall()
        db.commit()
    except sqlite3.IntegrityError as e:
        db.rollback()
        db.close()
        print(f"Encountered error executing query {command}, with parameters {params}. Error: {e}.")
        return (False, CONSTRAIN_FAILED)
    except Exception as e:
        db.rollback()
        db.close()
        print(f"Encountered error executing query {command}, with parameters {params}. Error: {e}.")
        return (False, OTHER)
    db.close()
    return (True, result)

def add_account(username: str, hashed_password):
    return query(
        "INSERT INTO Users (Id, Username, PasswordHash) VALUES (NULL, ?, ?)",
        username, 
        hashed_password
    )