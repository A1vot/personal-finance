from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from transactions.models import Transaction
from categories.models import Category
from django.db.models import Sum

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

    # Добавление транзакции
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')

        Transaction.objects.create(
            user=request.user,
            category_id=category_id,
            amount=amount,
            date=date,
            description=description
        )
        
        return redirect('/dashboard/')

    # Данные для отображения
    categories = Category.objects.all()
    transactions = Transaction.objects.filter(user=request.user)

    # Данные для отображения
    categories = Category.objects.all()
    transactions = Transaction.objects.filter(user=request.user)

    # Отчёт: расходы по категориям
    expense_report = (
        Transaction.objects
        .filter(user=request.user, category__type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    # Отчёт: доходы по категориям
    income_report = (
        Transaction.objects
        .filter(user=request.user, category__type='income')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    return render(request, 'pages/dashboard.html', {
        'categories': categories,
        'transactions': transactions,
        'expense_report': expense_report,
        'income_report': income_report
    })

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

# Удаление транзакции (только для владельца)
@login_required
def delete_transaction_view(request, transaction_id):
    Transaction.objects.filter(id=transaction_id, user=request.user).delete()
    return redirect('/dashboard/')
