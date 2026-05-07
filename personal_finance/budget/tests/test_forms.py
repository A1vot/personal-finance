from django.test import TestCase
from django.contrib.auth.models import User
from budget.forms import BudgetForm

class BudgetFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='123')

    def test_valid_form(self):
        form = BudgetForm(data={
            'monthly_limit': '5000.00'
        })
        self.assertTrue(form.is_valid())

    def test_missing_monthly_limit(self):
        form = BudgetForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('monthly_limit', form.errors)

    def test_invalid_monthly_limit(self):
        form = BudgetForm(data={
            'monthly_limit': 'abc'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('monthly_limit', form.errors)

    def test_zero_is_valid(self):
        form = BudgetForm(data={
            'monthly_limit': '0'
        })
        self.assertTrue(form.is_valid())

    def test_negative_value(self):
        form = BudgetForm(data={
            'monthly_limit': '-100'
        })
        # DecimalField допускает отрицательные числа, поэтому форма валидна
        self.assertTrue(form.is_valid())
