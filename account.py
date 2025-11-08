import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import database

def try_create_account(username : str, password : str, password_again : str) -> tuple:
    if password != password_again:
        return (False, "Salasanat eivät täsmää.")
    
    hash = generate_password_hash(password)
    try:
        database.add_account(username, hash)
    except sqlite3.IntegrityError as e:
        print(e)
        return (False, "Tunnus on jo käytössä. Kokeile toista nimeä.")
    except Exception as e:
        print(e)
        return (False, "Tunnusksen luonnissa tapahtui virhe.")
        
    return (True, None)

def check_password(username: str, password : str) -> bool:
    try:
        password_hash = database.get_password(username)
    except Exception as e:
        print(e)
        return False

    if len(password_hash) < 1:
        return False
    return check_password_hash(password_hash[0]["PasswordHash"], password)