import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from categories.models import Category
from transactions.models import Transaction


class TransactionModelTest(TestCase):
    """Тесты для модели Transaction."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            password="123",
        )
        self.category = Category.objects.create(
            name="Еда",
            type="expense",
        )

    def test_create_transaction(self):
        """Создание транзакции с корректными полями должно работать."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("150.50"),
            date=datetime.date(2024, 5, 1),
            description="Обед",
        )

        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, Decimal("150.50"))
        self.assertEqual(transaction.date, datetime.date(2024, 5, 1))
        self.assertEqual(transaction.description, "Обед")

    def test_str_method(self):
        """__str__ должен возвращать корректное строковое представление."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("100"),
            date=datetime.date(2024, 5, 1),
        )

        self.assertEqual(str(transaction), "Еда: 100 от 2024-05-01")

    def test_ordering(self):
        """Проверяем сортировку по дате: новые транзакции первыми."""
        t1 = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=10,
            date=datetime.date(2024, 5, 1),
        )
        t2 = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=20,
            date=datetime.date(2024, 5, 2),
        )

        transactions = list(Transaction.objects.all())
        self.assertEqual(transactions[0], t2)
        self.assertEqual(transactions[1], t1)
