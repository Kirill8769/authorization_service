from rest_framework import serializers

from users.models import User
from users.validators import InviteCodeValidator, PhoneValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    other_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'phone', 'my_invite_code', 'another_invite_code', 'other_users')
        validators = [
            PhoneValidator(phone_number='phone'),
        ]

    def get_other_users(self, obj):
        """Формирует поле с телефонами профилей применивших инвайт-код текущего пользователя."""

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            users = User.objects.filter(another_invite_code=user.my_invite_code).values('phone')
            return users


class InviteCodeSerializer(serializers.ModelSerializer):
    """Сериализатор активации инвайт-кода."""

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
