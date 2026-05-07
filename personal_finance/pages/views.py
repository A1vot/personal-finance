from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import Sum

from budget.models import Budget
from transactions.models import Transaction
from categories.models import Category

from transactions.forms import TransactionForm
from budget.forms import BudgetForm



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

    # Получаем или создаём бюджет пользователя
    budget, created = Budget.objects.get_or_create(user=request.user)

    # --- POST ---
    if request.method == 'POST':

        # 1) Обновление бюджета через ModelForm
        if 'monthly_limit' in request.POST:
            form_budget = BudgetForm(request.POST, instance=budget)
            if form_budget.is_valid():
                form_budget.save()
            return redirect('/dashboard/')

        # 2) Добавление транзакции через ModelForm
        form = TransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/dashboard/')

    else:
        form = TransactionForm()
        form_budget = BudgetForm(instance=budget)

    # --- Данные для отображения ---
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

    # Отчёты
    expense_report = (
        Transaction.objects
        .filter(user=request.user, category__type='expense', **period_filter)
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    income_report = (
        Transaction.objects
        .filter(user=request.user, category__type='income', **period_filter)
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    # Бюджет: расчёт остатка
    today = timezone.now()
    month_start = today.replace(day=1)

    monthly_expenses = (
        Transaction.objects
        .filter(user=request.user, date__gte=month_start, category__type='expense')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    remaining = budget.monthly_limit - monthly_expenses

    return render(request, 'pages/dashboard.html', {
        'categories': categories,
        'transactions': transactions,
        'expense_report': expense_report,
        'income_report': income_report,
        'budget': budget,
        'monthly_expenses': monthly_expenses,
        'remaining': remaining,
        'form': form,
        'form_budget': form_budget,
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
