from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from transactions.forms import TransactionForm


class TransactionFormTest(TestCase):
    """Тесты для формы транзакций TransactionForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            password="123",
        )
        self.category = Category.objects.create(
            name="Еда",
            type="expense",
        )

    def test_valid_form(self):
        """Форма валидна при корректных данных."""
        form = TransactionForm(data={
            "category": self.category.id,
            "amount": "150.50",
            "date": "2024-05-01",
            "description": "Обед",
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Отсутствие обязательных полей делает форму невалидной."""
        form = TransactionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)
        self.assertIn("amount", form.errors)
        self.assertIn("date", form.errors)

    def test_invalid_amount(self):
        """Некорректное значение amount должно вызвать ошибку."""
        form = TransactionForm(data={
            "category": self.category.id,
            "amount": "abc",
            "date": "2024-05-01",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)

    def test_invalid_date(self):
        """Некорректная дата должна вызвать ошибку."""
        form = TransactionForm(data={
            "category": self.category.id,
            "amount": "100",
            "date": "not-a-date",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_description_optional(self):
        """Описание является необязательным полем."""
        form = TransactionForm(data={
            "category": self.category.id,
            "amount": "100",
            "date": "2024-05-01",
            "description": "",
        })
        self.assertTrue(form.is_valid())
