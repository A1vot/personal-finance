import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from categories.models import Category
from transactions.models import Transaction


class TransactionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='123')
        self.category = Category.objects.create(
            name='Еда',
            type='expense'
        )

    def test_create_transaction(self):
        t = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('150.50'),
            date=datetime.date(2024, 5, 1),
            description='Обед'
        )

        self.assertEqual(t.user, self.user)
        self.assertEqual(t.category, self.category)
        self.assertEqual(t.amount, Decimal('150.50'))
        self.assertEqual(t.date, datetime.date(2024, 5, 1))
        self.assertEqual(t.description, 'Обед')

    def test_str_method(self):
        t = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100'),
            date=datetime.date(2024, 5, 1)
        )

        self.assertEqual(str(t), "Еда: 100 от 2024-05-01")

    def test_ordering(self):
        t1 = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=10,
            date=datetime.date(2024, 5, 1)
        )
        t2 = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=20,
            date=datetime.date(2024, 5, 2)
        )

        transactions = list(Transaction.objects.all())
        self.assertEqual(transactions[0], t2)
        self.assertEqual(transactions[1], t1)
