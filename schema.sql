CREATE TABLE Users
(
    Id INTEGER PRIMARY KEY,
    Username TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL
);

CREATE TABLE Recipes
(
    Name TEXT NOT NULL,
    Instructions TEXT NOT NULL,
    Ingredient TEXT NOT NULL
);