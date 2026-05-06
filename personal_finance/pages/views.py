from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# Страница входа (теперь с логикой авторизации)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Проверяем логин/пароль
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Авторизация пользователя
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Неверный логин или пароль')

    # GET-запрос → просто показываем форму
    return render(request, 'pages/login.html')


# Личный кабинет (доступен только авторизованным)
@login_required
def dashboard_view(request):
    return render(request, 'pages/dashboard.html')


# Регистрация нового пользователя
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Проверка совпадения паролей
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'pages/register.html')

        # Проверка существования пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь уже существует')
            return render(request, 'pages/register.html')

        # Создание пользователя
        User.objects.create_user(username=username, password=password)

        # После регистрации → на страницу входа
        return redirect('/')

    # GET-запрос → просто показываем форму
    return render(request, 'pages/register.html')
