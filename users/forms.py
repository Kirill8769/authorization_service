import re

from django import forms

from users.models import User


class UserAuthorizationForm(forms.ModelForm):
    phone = forms.CharField(max_length=12, label='Введите номер телефона', required=True)

    class Meta:
        model = User
        fields = ('phone', )

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        pattern = re.compile(r'^\+?7\d{10}$|^8\d{10}$')
        if not pattern.match(phone_number):
            raise forms.ValidationError(
                'Введите правильный номер телефона, формат номера: +71112223344, 87776665544, 75556667788'
            )
        return phone_number


class VerificationCodeForm(forms.Form):
    input_code = forms.CharField(max_length=4, label='Введите код верификации', required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_input_code(self):
        user_input_code = self.cleaned_data['input_code']
        verification_code = self.request.session.get('verification_code')
        if user_input_code != verification_code:
            raise forms.ValidationError('Введён неверный код верификации')
        return user_input_code


class UserDetailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('phone', 'my_invite_code', 'another_invite_code', )


class UserUpdateForm(forms.ModelForm):
    another_invite_code = forms.CharField(max_length=6, label='Введите инвайт-код', required=True)

    class Meta:
        model = User
        fields = ('another_invite_code', )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_another_invite_code(self):
        invite_codes = User.objects.values_list('my_invite_code', flat=True).exclude(my_invite_code=None)
        print(invite_codes)
        input_invite_code = self.cleaned_data['another_invite_code']
        print(input_invite_code)
        if input_invite_code and input_invite_code not in invite_codes:
            raise forms.ValidationError('Введённый инвайт-код не существует')
        if input_invite_code == self.user.my_invite_code:
            raise forms.ValidationError('Вы не можете использовать свой инвайт-код')
        if self.user.another_invite_code:
            raise forms.ValidationError('У Вас уже есть активированный инвайт-код')
        return input_invite_code
