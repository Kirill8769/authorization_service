from django.contrib.auth import login, logout
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, UpdateView, View
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.forms import UserAuthorizationForm, UserDetailForm, UserUpdateForm, VerificationCodeForm
from users.models import User
from users.permissions import IsUser
from users.serializers import InviteCodeSerializer, UserSerializer
from users.services import format_phone_number, generate_invite_code, send_verification_code


class UserAuthorizationView(TemplateView):
    """Контроллер формы авторизации."""

    template_name = 'users/user_authorization.html'
    success_url = reverse_lazy('users:user_verification')

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
        phone_number = format_phone_number(form.cleaned_data['phone'])
        user, created = User.objects.get_or_create(phone=phone_number)
        if created:
            user.my_invite_code = generate_invite_code()
            user.save()
        verification_code = send_verification_code(phone_number=phone_number)
        self.save_session(phone_number=phone_number, verification_code=verification_code)
        return redirect(self.success_url)

    def form_invalid(self, form):
        phone_number = form['phone'].value()
        formatted_phone_number = format_phone_number(phone_number)
        if User.objects.filter(phone=formatted_phone_number).exists():
            verification_code = send_verification_code(phone_number=formatted_phone_number)
            self.save_session(phone_number=phone_number, verification_code=verification_code)
            return redirect(self.success_url)
        return self.render_to_response({'form': form})

    def save_session(self, phone_number: str, verification_code: str) -> None:
        """
        Сохраняет необходимые данные в сессию.

        :param phone_number: Номер телефона.
        :param verification_code: Код верификации.
        :return: None
        """

        self.request.session['phone_number'] = phone_number
        self.request.session['verification_code'] = verification_code


class UserVerificationPhoneView(TemplateView):
    """Контроллер формы верификации пользователя."""

    template_name = 'users/user_verification.html'
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
        user = User.objects.filter(phone=phone_number).first()
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


class UserLogoutView(View):
    """Контроллер формы выхода из профиля."""

    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)


class UserDetailView(DetailView):
    """Контроллер формы детального просмотра профиля."""

    template_name = 'users/user_detail.html'
    form_class = UserDetailForm
    queryset = User.objects.all()


class UserUpdateView(UpdateView):
    """Контроллер формы изменения профиля."""

    form_class = UserUpdateForm
    success_url = reverse_lazy('main:index')
    queryset = User.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserAuthorizationAPIView(APIView):
    """Контроллер авторизации пользователя по API."""

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.data.get('phone')
            formatted_phone_number = format_phone_number(phone_number=phone_number)
            user, created = User.objects.get_or_create(phone=formatted_phone_number)
            if created:
                user.my_invite_code = generate_invite_code()
                user.save()
            verification_code = send_verification_code(phone_number=formatted_phone_number)
            cache.set(formatted_phone_number, verification_code, timeout=600)
            verification_code = cache.get(formatted_phone_number)
            message = {
                'id': user.pk,
                'phone': user.phone,
                'my_invite_code': user.my_invite_code,
                'another_invite_code': user.another_invite_code,
                'verification_code': verification_code,
            }
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerificationAPIView(APIView):
    """Контроллер верификации пользователя по API."""

    def post(self, request):
        phone_number = request.data.get('phone')
        formatted_phone_number = format_phone_number(phone_number=phone_number)
        if not User.objects.filter(phone=formatted_phone_number).exists():
            return Response(
                {'error': 'Указанный номер телефона не зарегистрирован'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data_code = request.data.get('code', None)
        if data_code is None:
            return Response(
                {'error': 'Добавьте ключ code и в значении укажите код верификации'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        verification_code = cache.get(formatted_phone_number)
        if str(data_code) != verification_code:
            return Response(
                {'error': 'Код верификации недействителен'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(phone=formatted_phone_number).first()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': 'Вы успешно авторизованы',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserListAPIView(ListAPIView):
    """Контроллер вывода списка пользователей по API."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """Контроллер просмотра профиля по API."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


class UserUpdateAPIView(UpdateAPIView):
    """Контроллер изменения профиля по API."""

    serializer_class = InviteCodeSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]

    def get_serializer(self, *args, **kwargs):
        kwargs['user'] = self.request.user
        return super().get_serializer(*args, **kwargs)
