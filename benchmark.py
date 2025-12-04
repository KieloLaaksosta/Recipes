import random
import sqlite3
from werkzeug.security import generate_password_hash
import database

db = sqlite3.connect("database.db")
connection = database.get_connection()

USER_COUNT = 1000
RECIPE_COUNT = 10**5
TAG_COUNT = 6
REVIEW_COUNT = 10**6

for i in range(1, USER_COUNT + 1):
    database.query(
        "INSERT INTO Users (Id, Username, PasswordHash) VALUES (NULL, ?, ?)",
        ["user" + str(i), generate_password_hash(str(i))],
        connection
    )

for i in range(1, RECIPE_COUNT + 1):
    database.query(
        "INSERT INTO Recipes (Id, Name, CreatorId, Instructions, Ingredients) VALUES (NULL, ?, ?, ?, ?)",
        ["name" + str(i), random.randint(1, USER_COUNT), "instrucitons" + str(i), "ingredients" + str(i)],
        connection
    )
    
    for j in range(1, TAG_COUNT + 1):
        if random.randint(0, 2) == 0:
            database.query(
                "INSERT INTO TagJoin (RecipeId, TagId) VALUES (?, ?)",
                [i, j],
                connection
            )

for i in range(1, REVIEW_COUNT + 1):
    database.query(
        """
        INSERT INTO Reviews (Id, RecipeId, ReviewerId, Rating, Comment)
        VALUES (NULL, ?, ?, ?, ?)
        """,
        [random.randint(1, RECIPE_COUNT), random.randint(1, USER_COUNT), random.randint(1, 5), "comment" + str(i)],
        connection
    )

connection.commit()
connection.close()
print("READY")
