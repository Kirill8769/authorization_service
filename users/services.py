import string
from random import choice


def format_phone_number(phone_number, country='RU'):
    countries = {
        'RU': '+7',
    }
    format_number = f'{countries[country]}{phone_number[-10:]}'
    return format_number


def generate_invite_code(length=6):
    simbols = string.ascii_letters + string.digits
    invite_code = ''.join(choice(simbols) for _ in range(length))
    return invite_code
