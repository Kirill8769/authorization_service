import string
import time
import uuid
from random import randint
from random import choice


def format_phone_number(phone_number: str, country: str = 'RU') -> str:
    """
    Фрматирует номер телефона и возвращает его страндартизированном виде.

    :param phone_number: Номер телефона.
    :param country: Страна, для определения кода.
    :return: Отформатированный номер телефона.
    """

    countries = {'RU': '+7', }
    try:
        format_number = f'{countries[country]}{phone_number[-10:]}'
    except Exception:
        format_number = "+71112223344"
    return format_number


def send_verification_code(phone_number: str) -> str:
    """
    Отправляет код верификации на переданный номер телефона, но пока только возвращает.

    :param phone_number: Номер телефона.
    :return: Код верификации.
    """
    time.sleep(randint(1, 2))
    verification_code = str(uuid.uuid4().int)[:4]
    return verification_code


def generate_invite_code(length: int = 6) -> str:
    """
    Генерирует и возвращает инвайт-код.

    :param length: Ожидаемая длинна инвайт-кода.
    :return: Сгенерированный инвайт-код.
    """
    simbols = string.ascii_letters + string.digits
    invite_code = ''.join(choice(simbols) for _ in range(length))
    return invite_code
