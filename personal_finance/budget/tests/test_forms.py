from django.test import TestCase
from django.contrib.auth.models import User
from budget.forms import BudgetForm


class BudgetFormTest(TestCase):
    """Тесты для формы бюджета BudgetForm."""

    def setUp(self):
        # Создаём пользователя (если в будущем понадобится привязка)
        self.user = User.objects.create_user(
            username="alex",
            password="123"
        )

    def test_valid_form(self):
        """Форма валидна при корректном значении monthly_limit."""
        form = BudgetForm(data={"monthly_limit": "5000.00"})
        self.assertTrue(form.is_valid())

    def test_missing_monthly_limit(self):
        """monthly_limit — обязательное поле, отсутствие делает форму невалидной."""
        form = BudgetForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("monthly_limit", form.errors)

    def test_invalid_monthly_limit(self):
        """Невалидное значение (строка вместо числа) должно вызвать ошибку."""
        form = BudgetForm(data={"monthly_limit": "abc"})
        self.assertFalse(form.is_valid())
        self.assertIn("monthly_limit", form.errors)

    def test_zero_is_valid(self):
        """Нулевой лимит допустим — DecimalField принимает 0."""
        form = BudgetForm(data={"monthly_limit": "0"})
        self.assertTrue(form.is_valid())

    def test_negative_value(self):
        """Отрицательные значения допустимы, т.к. ограничений в модели нет."""
        form = BudgetForm(data={"monthly_limit": "-100"})
        self.assertTrue(form.is_valid())
