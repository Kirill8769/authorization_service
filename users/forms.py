import re

from django import forms

from users.models import User


class UserForm(forms.ModelForm):
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


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('phone', 'my_invite_code', 'another_invite_code', )


class VerifyForm(forms.BaseForm):

    class Meta:
        verification_code = forms.CharField(max_length=4, help_text='vvedite cod')
