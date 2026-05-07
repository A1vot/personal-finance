from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from budget.models import Budget


class BudgetModelTest(TestCase):
    """Тесты для модели бюджета Budget."""

    def setUp(self):
        # Создаём пользователя для привязки бюджета
        self.user = User.objects.create_user(
            username="alex",
            password="123"
        )

    def test_create_budget(self):
        """Создание бюджета с указанным лимитом должно работать корректно."""
        budget = Budget.objects.create(
            user=self.user,
            monthly_limit=Decimal("50000.00")
        )

        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.monthly_limit, Decimal("50000.00"))

    def test_default_monthly_limit(self):
        """Если monthly_limit не указан, должен использоваться default=0."""
        budget = Budget.objects.create(user=self.user)
        self.assertEqual(budget.monthly_limit, Decimal("0"))

    def test_str_method(self):
        """__str__ должен возвращать 'Бюджет <username>'."""
        budget = Budget.objects.create(
            user=self.user,
            monthly_limit=10000
        )

        self.assertEqual(str(budget), "Бюджет alex")

    def test_ordering(self):
        """Проверяем сортировку: сначала по user, затем по monthly_limit."""
        user2 = User.objects.create_user(username="bob", password="123")

        b1 = Budget.objects.create(user=self.user, monthly_limit=100)
        b2 = Budget.objects.create(user=user2, monthly_limit=50)

        budgets = list(Budget.objects.all())

        self.assertEqual(budgets[0], b1)
        self.assertEqual(budgets[1], b2)
