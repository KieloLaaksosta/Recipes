from werkzeug.security import generate_password_hash, check_password_hash
import database

def try_create_account(username : str, password : str, password_again : str) -> tuple:
    if password != password_again:
        return (False, "Salasanat eivät täsmää.")
    
    hash = generate_password_hash(password)
    successful, error_reason = database.add_account(username, hash)
    if not successful:
        if error_reason == database.CONSTRAIN_FAILED:
            return (False, "Tunnus on jo käytössä. Kokeile toista nimeä.")
        else:
            return (False, "Käyttäjän luonnissa tapahtui virhe.")
        
    return (True, None)

def check_password(username: str, password : str):
    successfull, password_hash = database.get_password(username)
    return successfull and check_password_hash(password_hash[0][0], password)