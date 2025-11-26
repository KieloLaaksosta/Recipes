import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, session, redirect
import database, validation

def try_create_account(username : str, password : str, password_again : str) -> tuple:
    if password != password_again:
        return "Salasanat eivät täsmää."
    
    hash = generate_password_hash(password)
    try:
        database.add_account(username, hash)
    except sqlite3.IntegrityError as e:
        print(e)
        return "Tunnus on jo käytössä. Kokeile toista nimeä."
    except Exception as e:
        print(e)
        return "Tunnusksen luonnissa tapahtui virhe."
        
    return None

def check_password(username: str, password : str) -> bool:
    try:
        password_hash = database.get_password(username)
    except Exception as e:
        print(e)
        return False

    if len(password_hash) < 1:
        return False
    return check_password_hash(password_hash[0]["PasswordHash"], password)

def register_get():
    return render_template("register.html")

def register_post(username: str, password: str, password_again: str):
    error_code, username = validation.limit_lenght(username, validation.MIN_USERNAME_LENGTH, validation.MAX_USERNAME_LENGTH)
    if(validation.contains_whitespace(username)):
        error_msg = "Käyttäjänimessä ei saa olla välilyöntejä tai rivinvaihtoja,"

    error_msg = None

    if error_code != validation.VALID:
        if error_code == validation.INVALID_TYPE:
            error_msg = f"Käyttänimi tulee antaa."
        if error_code == validation.TOO_LONG:
            error_msg = f"Käyttänimen tulee olla enintään {validation.MAX_USERNAME_LENGTH} merkkiä pitkä."
        if error_code == validation.TOO_SHORT:
            error_msg = f"Käyttänimen tulee olla vähintään {validation.MIN_USERNAME_LENGTH} merkkiä pitkä."
    
    error_code, password = validation.limit_lenght(password, validation.MIN_PASSWORD_LENGHT, validation.MAX_PASSWORD_LENGHT)
    if error_code != validation.VALID:
        if error_code == validation.INVALID_TYPE:
            error_msg = "Salasana tulee antaa."
        if error_code == validation.TOO_SHORT:
            error_msg = f"Salasanan tulee olla vähintään {validation.MIN_PASSWORD_LENGHT} merkkiä pitkä."
        if error_code == validation.TOO_LONG:
            error_msg = f"Salasanan tulee olla enintään {validation.MAX_PASSWORD_LENGHT} merkkiä pitkä."

    _, password_again = validation.limit_lenght(password_again, max=validation.MAX_PASSWORD_LENGHT)

    if not error_msg:
        error_msg = try_create_account(username, password, password_again)
    
    if error_msg == None:
        session["username"] = username
        session["user_id"] = database.get_user_id(username)[0]["Id"]

    if error_msg:
        return render_template("register.html", error_msg=error_msg)
    else:
        return redirect("/")

def login_post(username: str, password: str):
    _, username = validation.limit_lenght(username, validation.MIN_USERNAME_LENGTH, validation.MAX_USERNAME_LENGTH)
    _, password = validation.limit_lenght(password, validation.MIN_USERNAME_LENGTH, validation.MAX_USERNAME_LENGTH)

    if check_password(username, password):
        session["username"] = username
        session["user_id"] = database.get_user_id(username)[0]["Id"]
        return redirect("/")
    else:
        error_msg = "Väärä käyttäjätunnus tai salasana"
        return render_template("error_pages/login_account.html", error_msg)

def login_get():
    return render_template("login.html")

def log_out():
    del session["username"]
    return redirect("/")