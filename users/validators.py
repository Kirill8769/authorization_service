import re

from rest_framework.exceptions import ValidationError

from users.models import User


class PhoneValidator:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def __call__(self, values):
        phone_number = dict(values).get(self.phone_number)
        pattern = re.compile(r'^\+?7\d{10}$|^8\d{10}$')
        if not pattern.match(phone_number):
            raise ValidationError(
                'Введите правильный номер телефона, формат номера: +71112223344, 87776665544, 75556667788'
            )


class InviteCodeValidator:

    def __init__(self, user):
        self.user = user

    def __call__(self, input_code):
        invite_codes = User.objects.values_list('my_invite_code', flat=True).exclude(my_invite_code=None)
        if input_code and input_code not in invite_codes:
            raise ValidationError('Введённый инвайт-код не существует')
        if input_code == self.user.my_invite_code:
            raise ValidationError('Вы не можете использовать свой инвайт-код')
        if self.user.another_invite_code:
            raise ValidationError('У Вас уже есть активированный инвайт-код')
        return input_code
