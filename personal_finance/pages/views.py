from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

from budget.models import Budget
from categories.models import Category
from transactions.models import Transaction

from transactions.forms import TransactionForm
from budget.forms import BudgetForm


def login_view(request):
    """Страница входа с обработкой POST-авторизации."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        messages.error(request, "Неверный логин или пароль")

    return render(request, "pages/login.html")


@login_required
def dashboard_view(request):
    """Личный кабинет: бюджет, транзакции, отчёты, фильтры."""
    budget, _ = Budget.objects.get_or_create(user=request.user)

    # POST
    if request.method == "POST":

        # Обновление бюджета
        if "monthly_limit" in request.POST:
            form_budget = BudgetForm(request.POST, instance=budget)
            if form_budget.is_valid():
                form_budget.save()
            return redirect("/dashboard/")

        # Добавление транзакции
        form = TransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("/dashboard/")

    else:
        form = TransactionForm()
        form_budget = BudgetForm(instance=budget)

    # --- Фильтр периода ---
    start_date = request.GET.get("start")
    end_date = request.GET.get("end")

    period_filter = {}
    if start_date:
        period_filter["date__gte"] = start_date
    if end_date:
        period_filter["date__lte"] = end_date

    transactions = Transaction.objects.filter(
        user=request.user,
        **period_filter,
    )

    # Отчёты
    expense_report = (
        Transaction.objects
        .filter(user=request.user, category__type="expense", **period_filter)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    income_report = (
        Transaction.objects
        .filter(user=request.user, category__type="income", **period_filter)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    # Бюджет: расчёт остатка
    today = timezone.now()
    month_start = today.replace(day=1)

    monthly_expenses = (
        Transaction.objects
        .filter(user=request.user, date__gte=month_start, category__type="expense")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    remaining = budget.monthly_limit - monthly_expenses

    return render(
        request,
        "pages/dashboard.html",
        {
            "categories": Category.objects.all(),
            "transactions": transactions,
            "expense_report": expense_report,
            "income_report": income_report,
            "budget": budget,
            "monthly_expenses": monthly_expenses,
            "remaining": remaining,
            "form": form,
            "form_budget": form_budget,
        },
    )


def register_view(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Пароли не совпадают")
            return render(request, "pages/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь уже существует")
            return render(request, "pages/register.html")

        User.objects.create_user(username=username, password=password)
        return redirect("/")

    return render(request, "pages/register.html")


@login_required
def delete_transaction_view(request, transaction_id):
    """Удаление транзакции, принадлежащей текущему пользователю."""
    Transaction.objects.filter(id=transaction_id, user=request.user).delete()
    return redirect("/dashboard/")
