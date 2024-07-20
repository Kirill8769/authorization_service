from rest_framework import serializers

from users.models import User
from users.validators import PhoneValidator, InviteCodeValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'phone', 'my_invite_code', 'another_invite_code', )
        validators = [
            PhoneValidator(phone_number='phone'),
        ]


class InviteCodeSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def validate(self, data):
        validator = InviteCodeValidator(user=self.user)
        validator(data['another_invite_code'])
        return data

    class Meta:
        model = User
        fields = ('another_invite_code', )
