MAX_INSCTRUCTIONS_LENGHT = 65536
MAX_INGREDIENTS_LENGHT = 65536
MAX_SEARCH_LENGHT = 65536
MAX_MAX_COMMENT_LENGHT = 65536

MIN_PASSWORD_LENGHT = 8
MAX_PASSWORD_LENGHT = 255

MIN_USERNAME_LENGHT = 1
MAX_USERNAME_LENGHT = 255

VALID = 0
TOO_SHORT = 1
TOO_LONG = 2
INVALID_TYPE = 3

MAX_RECIPE_NAME_LENGHT = 255
MIN_RECIPE_NAME_LENGHT = 1



def limit_lenght(string: str, min: int = 0, max: int = 65536) -> tuple:
    if type(string) is not str or string == None:
        return (-2, "")
    
    if len(string) < min:
        return (TOO_SHORT, string)
    if len(string) > max:
        return (TOO_LONG, string[:max])

    return (VALID, string)

def contains_whitespace(string: str) -> bool:
    return False

def clamp_rating(rating: int):
    return min(max(rating, 1), 5)

def truncate_list(values: list, n: int = 255) -> list:
    return values[:n]

def trim_limit_lenght(string: str, n: int) -> str:
    if type(string) is not str or string == None:
        return None
    
    string = string.strip()
    if(len(string) == 0):
        return None

    return string[:min(n, len(string))]