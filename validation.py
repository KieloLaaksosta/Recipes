MAX_INSCTRUCTIONS_LENGTH = 65536
MAX_INGREDIENTS_LENGTH = 65536
MAX_SEARCH_LENGTH = 32
MAX_MAX_COMMENT_LENGTH = 65536

MIN_PASSWORD_LENGHT = 3
MAX_PASSWORD_LENGHT = 255

MIN_USERNAME_LENGTH = 1
MAX_USERNAME_LENGTH = 255

VALID = 0
TOO_SHORT = 1
TOO_LONG = 2
INVALID_TYPE = 3

MAX_RECIPE_NAME_LENGTH = 32
MIN_RECIPE_NAME_LENGTH = 1



def limit_lenght(string: str, min_len: int = 0, max_len: int = 65536) -> tuple:
    if not isinstance(string, str) or string is None:
        return (-2, "")

    if len(string) < min_len:
        return (TOO_SHORT, string)
    if len(string) > max_len:
        return (TOO_LONG, string[:max_len])

    return (VALID, string)

def contains_whitespace(string: str) -> bool:
    return any(char.isspace() for char in string)

def clamp_rating(rating: int):
    return min(max(rating, 1), 5)

def truncate_list(values: list, n: int = 255) -> list:
    return values[:n]

def trim_limit_lenght(string: str, n: int) -> str:
    if not isinstance(string, str) is not str or string is None:
        return None

    string = string.strip()
    if len(string) == 0:
        return None

    return string[:min(n, len(string))]
