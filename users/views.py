import string
from random import choice, randint

from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, View

from users.forms import UserAuthorizationForm, VerificationCodeForm, UserUpdateForm
from users.models import User


class UserInputPhone(TemplateView):
    template_name = 'users/user_authorization.html'
    success_url = reverse_lazy('users:verification_phone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserAuthorizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UserAuthorizationForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone']
        user = User.objects.create(phone=phone_number, password='V3oigTerFFd0Fe')
        user.my_invite_code = self.generate_invite_code()
        user.save()
        self.send_verification_code(phone_number=phone_number)
        return redirect(self.success_url)

    def form_invalid(self, form):
        phone_number = form['phone'].value()
        if User.objects.filter(phone__contains=phone_number[-10:]).exists():
            self.send_verification_code(phone_number=phone_number)
            return redirect(self.success_url)
        return self.render_to_response({'form': form})

    def send_verification_code(self, phone_number):
        verification_code = str(randint(1000, 9999))
        self.request.session['phone_number'] = phone_number
        self.request.session['verification_code'] = verification_code

    @staticmethod
    def generate_invite_code(length=6):
        simbols = string.ascii_letters + string.digits
        invite_code = ''.join(choice(simbols) for _ in range(length))
        print(invite_code)
        return invite_code


class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        return super().form_valid(form)


class UserVerificationPhone(TemplateView):
    template_name = 'users/verification_phone.html'
    form_class = VerificationCodeForm
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        user = User.objects.filter(phone__contains=phone_number[-10:])[0]
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        print('invalid', self.request.session['verification_code'])
        return self.render_to_response({'form': form})


class UserLogoutView(View):
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)
