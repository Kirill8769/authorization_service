from random import randint

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import UserForm, VerifyForm
from users.models import User


class UserAuthorization(TemplateView):
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:verify_phone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        print('Создание нового пользователя')
        phone_number = form['phone']
        print(phone_number)
        User.objects.create(phone=phone_number)
        return redirect('users:user_create')

    def form_invalid(self, form):
        print('invalid')
        return self.render_to_response({'form': form})

    def send_verification_code(self, phone_number):
        verification_code = randint(1000, 9999)
        self.extra_context = {'info': f'Код верификации: {verification_code}'}
        print(verification_code)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:main')

    def form_valid(self, form):
        response = super().form_valid(form)
        # generate invite code
        return response


class UserVerifyPhone(TemplateView):
    template_name = 'users/verify_phone.html'
    form_class = VerifyForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']

            if self.verify_code(verification_code):
                # Логика успешной верификации
                return redirect('users:main')
            else:
                form.add_error('verification_code', 'Неверный код верификации')
            return self.render_to_response({'form': form})

    def verify_code(self, code):
        # Логика проверки кода верификации
        return True
