from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from budget.models import Budget


class BudgetModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='123')

    def test_create_budget(self):
        b = Budget.objects.create(
            user=self.user,
            monthly_limit=Decimal('50000.00')
        )

        self.assertEqual(b.user, self.user)
        self.assertEqual(b.monthly_limit, Decimal('50000.00'))

    def test_default_monthly_limit(self):
        b = Budget.objects.create(user=self.user)
        self.assertEqual(b.monthly_limit, Decimal('0'))

    def test_str_method(self):
        b = Budget.objects.create(
            user=self.user,
            monthly_limit=10000
        )

        self.assertEqual(str(b), "Бюджет alex")

    def test_ordering(self):
        u2 = User.objects.create_user(username='bob', password='123')

        b1 = Budget.objects.create(user=self.user, monthly_limit=100)
        b2 = Budget.objects.create(user=u2, monthly_limit=50)

        budgets = list(Budget.objects.all())

        # Сортировка: сначала по user, затем по monthly_limit
        self.assertEqual(budgets[0], b1)
        self.assertEqual(budgets[1], b2)
