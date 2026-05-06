from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from budget.models import Budget

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

        # 1. Изменение бюджета
        if 'budget' in request.POST:
            raw = request.POST.get('budget')

            # Если поле пустое — ничего не меняем
            if raw:
                budget, created = Budget.objects.get_or_create(user=request.user)
                budget.monthly_limit = raw
                budget.save()

            return redirect('/dashboard/')

        # 2. Добавление транзакции
        if 'category' in request.POST:
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
    
    # Фильтр периода
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    period_filter = {}

    if start_date:
        period_filter['date__gte'] = start_date

    if end_date:
        period_filter['date__lte'] = end_date

    # Отчёт: расходы по категориям
    expense_report = (
        Transaction.objects
        .filter(
            user=request.user,
            category__type='expense',
            **period_filter
        )
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    # Отчёт: доходы по категориям
    income_report = (
        Transaction.objects
        .filter(
            user=request.user,
            category__type='income',
            **period_filter
        )
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    
    # Текущий месяц
    today = timezone.now()
    month_start = today.replace(day=1)

    # Расходы за текущий месяц
    monthly_expenses = (
        Transaction.objects
        .filter(user=request.user, date__gte=month_start, category__type='expense')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    # Бюджет пользователя
    budget, created = Budget.objects.get_or_create(user=request.user)

    # Остаток
    remaining = budget.monthly_limit - monthly_expenses

    return render(request, 'pages/dashboard.html', {
        'categories': categories,
        'transactions': transactions,
        'expense_report': expense_report,
        'income_report': income_report,
        'budget': budget,
        'monthly_expenses': monthly_expenses,
        'remaining': remaining
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
