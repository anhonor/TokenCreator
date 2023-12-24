import random
import string

def __get_date_of_birth__(before: int = 2000, after: int = 1950) -> str:
    return f'{random.randint(after, before)}-{"{:02d}".format(random.randint(1, 12))}-{"{:02d}".format(random.randint(1, 25))}'

def __get_random_string__(length: int, include_digits: bool = False) -> None:
    return ''.join(random.choice(string.ascii_letters + string.digits if include_digits else string.ascii_letters) for letter in range(length))

def __get_random_email_provider__() -> str:
    return random.choice([
        '@gmail.com',
        '@mail.com',
        '@windstream.net',
        '@yahoo.com',
        '@hotmail.com',
        '@outlook.com'
    ])
