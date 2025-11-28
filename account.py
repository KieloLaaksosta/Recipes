import sqlite3, secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, session
import database, validation

def try_create_account(username : str, password : str) -> tuple:    
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
    error_msgs = []
    if(validation.contains_whitespace(username)):
        error_msgs.append("Käyttäjänimessä ei saa olla välilyöntejä tai rivinvaihtoja.")

    if error_code != validation.VALID:
        if error_code == validation.INVALID_TYPE:
            error_msgs.append("Käyttänimi tulee antaa.")
        if error_code == validation.TOO_LONG:
            error_msgs.append(f"Käyttänimen tulee olla enintään {validation.MAX_USERNAME_LENGTH} merkkiä pitkä.")
        if error_code == validation.TOO_SHORT:
            error_msgs.append(f"Käyttänimen tulee olla vähintään {validation.MIN_USERNAME_LENGTH} merkkiä pitkä.")
    
    error_code, password = validation.limit_lenght(password, validation.MIN_PASSWORD_LENGHT, validation.MAX_PASSWORD_LENGHT)
    if error_code != validation.VALID:
        if error_code == validation.INVALID_TYPE:
            error_msgs.append("Salasana tulee antaa.")
        if error_code == validation.TOO_SHORT:
            error_msgs.append(f"Salasanan tulee olla vähintään {validation.MIN_PASSWORD_LENGHT} merkkiä pitkä.")
        if error_code == validation.TOO_LONG:
            error_msgs.append(f"Salasanan tulee olla enintään {validation.MAX_PASSWORD_LENGHT} merkkiä pitkä.")

    _, password_again = validation.limit_lenght(password_again, max=validation.MAX_PASSWORD_LENGHT)

    if password != password_again:
        error_msgs.append("Salasanat eivät täsmää.")

    print(error_msgs)

    if len(error_msgs) == 0:
        new_error = try_create_account(username, password, password_again)
        if new_error:
            error_msgs.append(new_error)
    
    if len(error_msgs) == 0:
        session["username"] = username
        session["user_id"] = database.get_user_id(username)[0]["Id"]
        session["csfr_token"] = secrets.token_hex(16)

    if len(error_msgs) != 0:
        return render_template(
            "register.html", 
            error_msgs=error_msgs,
            username=username,
            password=password,
            password_again=password_again,
            max_username_len=validation.MAX_USERNAME_LENGTH,
            max_password_len=validation.MAX_PASSWORD_LENGHT
        )
    else:
        return redirect("/")

def login_post(username: str, password: str):
    _, username = validation.limit_lenght(username, validation.MIN_USERNAME_LENGTH, validation.MAX_USERNAME_LENGTH)
    _, password = validation.limit_lenght(password, validation.MIN_USERNAME_LENGTH, validation.MAX_USERNAME_LENGTH)

    if check_password(username, password):
        session["username"] = username
        session["user_id"] = database.get_user_id(username)[0]["Id"]
        session["csfr_token"] = secrets.token_hex(16)

        return redirect("/")
    else:
        return render_template(
            "login.html", 
            error_msg="Väärä käyttäjätunnus tai salasana",
            username=username,
            password=password,
            max_username_len=validation.MAX_USERNAME_LENGTH,
            max_password_len=validation.MAX_PASSWORD_LENGHT
        )

def login_get():
    return render_template(
        "login.html",
        max_username_len=validation.MAX_USERNAME_LENGTH,
        max_password_len=validation.MAX_PASSWORD_LENGHT
    )

def log_out():
    del session["username"]
    del session["user_id"]
    del session["csfr_token"]
    return redirect("/")