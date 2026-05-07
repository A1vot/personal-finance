from django.test import TestCase
from categories.models import Category


class CategoryModelTest(TestCase):

    def test_create_category(self):
        c = Category.objects.create(
            name='Еда',
            type='expense'
        )

        self.assertEqual(c.name, 'Еда')
        self.assertEqual(c.type, 'expense')

    def test_unique_name(self):
        Category.objects.create(name='Еда', type='expense')

        with self.assertRaises(Exception):
            Category.objects.create(name='Еда', type='income')

    def test_str_method(self):
        c = Category.objects.create(
            name='Зарплата',
            type='income'
        )

        self.assertEqual(str(c), "Зарплата (Доход)")

    def test_ordering(self):
        c1 = Category.objects.create(name='Еда', type='expense')
        c2 = Category.objects.create(name='Зарплата', type='income')
        c3 = Category.objects.create(name='Авто', type='expense')

        categories = list(Category.objects.all())

        # Сначала доходы, потом расходы
        self.assertEqual(categories[0], c2)

        # Внутри расходов — сортировка по name
        self.assertEqual(categories[1], c3)  # Авто
        self.assertEqual(categories[2], c1)  # Еда
