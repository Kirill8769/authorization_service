import time
from random import randint

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import UserForm, VerificationCodeForm
from users.models import User


class UserAuthorization(TemplateView):
    template_name = 'users/verification_phone.html'
    success_url = reverse_lazy('users:verification_phone')

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
        phone_number = form.cleaned_data['phone']
        print(phone_number)
        User.objects.create(phone=phone_number)
        self.send_verification_code(phone_number=phone_number)
        return redirect(self.success_url)

    def form_invalid(self, form):
        print('invalid')
        phone_number = form['phone'].value()
        print(phone_number)
        if User.objects.filter(phone__contains=phone_number[-10:]).exists():
            print('user uje est')
            self.send_verification_code(phone_number=phone_number)
            return redirect(self.success_url)
        return self.render_to_response({'form': form})

    def send_verification_code(self, phone_number):
        verification_code = randint(1000, 9999)
        self.request.session['phone_number'] = phone_number
        self.request.session['verification_code'] = verification_code
        print('send', self.request.session)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
#     success_url = reverse_lazy('users:main')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # generate invite code
#         return response


class UserVerificationPhone(TemplateView):
    template_name = 'users/verification_phone.html'
    form_class = VerificationCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        print('ver', form['input_code'].value())
        print('r', request)
        if form.is_valid():
            print(111)
        print(222)
        return self.render_to_response({'form': form})
