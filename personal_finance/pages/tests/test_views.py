from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from budget.models import Budget
from categories.models import Category
from transactions.models import Transaction


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='123')

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_valid_post(self):
        response = self.client.post(reverse('login'), {
            'username': 'alex',
            'password': '123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_login_invalid_post(self):
        response = self.client.post(reverse('login'), {
            'username': 'alex',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверный логин или пароль')


class RegisterViewTest(TestCase):

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': '123',
            'password2': '456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пароли не совпадают')

    def test_register_existing_user(self):
        User.objects.create_user(username='alex', password='123')
        response = self.client.post(reverse('register'), {
            'username': 'alex',
            'password': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователь уже существует')


class DashboardViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='123')
        self.category = Category.objects.create(name='Еда', type='expense')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/?next=/dashboard/', response.url)

    def test_dashboard_get(self):
        self.client.login(username='alex', password='123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)
        self.assertIn('transactions', response.context)
        self.assertIn('budget', response.context)

    def test_update_budget(self):
        self.client.login(username='alex', password='123')
        response = self.client.post(reverse('dashboard'), {
            'monthly_limit': '5000'
        })
        self.assertEqual(response.status_code, 302)
        budget = Budget.objects.get(user=self.user)
        self.assertEqual(budget.monthly_limit, 5000)

    def test_add_transaction(self):
        self.client.login(username='alex', password='123')
        response = self.client.post(reverse('dashboard'), {
            'category': self.category.id,
            'amount': '150',
            'date': '2024-05-01',
            'description': 'Обед'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_date_filter(self):
        self.client.login(username='alex', password='123')

        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=100,
            date='2024-05-01'
        )

        response = self.client.get(reverse('dashboard') + '?start=2024-05-02')
        self.assertEqual(len(response.context['transactions']), 0)


class DeleteTransactionViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alex', password='123')
        self.category = Category.objects.create(name='Еда', type='expense')
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=100,
            date='2024-05-01'
        )

    def test_delete_requires_login(self):
        response = self.client.get(f'/transactions/delete/{self.transaction.id}/')
        self.assertEqual(response.status_code, 302)

    def test_delete_own_transaction(self):
        self.client.login(username='alex', password='123')
        response = self.client.get(f'/transactions/delete/{self.transaction.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_delete_not_own_transaction(self):
        User.objects.create_user(username='bob', password='123')
        self.client.login(username='bob', password='123')
        self.client.get(f'/transactions/delete/{self.transaction.id}/')
        self.assertEqual(Transaction.objects.count(), 1)
