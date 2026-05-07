from django.test import TestCase
from categories.models import Category


class CategoryModelTest(TestCase):
    """Тесты для модели Category."""

    def test_create_category(self):
        """Создание категории с корректными полями должно работать."""
        category = Category.objects.create(
            name="Еда",
            type="expense",
        )

        self.assertEqual(category.name, "Еда")
        self.assertEqual(category.type, "expense")

    def test_unique_name(self):
        """Имя категории должно быть уникальным."""
        Category.objects.create(name="Еда", type="expense")

        with self.assertRaises(Exception):
            Category.objects.create(name="Еда", type="income")

    def test_str_method(self):
        """__str__ должен возвращать корректное строковое представление."""
        category = Category.objects.create(
            name="Зарплата",
            type="income",
        )

        self.assertEqual(str(category), "Зарплата (Доход)")

    def test_ordering(self):
        """Проверяем сортировку: доходы → расходы, внутри — по имени."""
        c1 = Category.objects.create(name="Еда", type="expense")
        c2 = Category.objects.create(name="Зарплата", type="income")
        c3 = Category.objects.create(name="Авто", type="expense")

        categories = list(Category.objects.all())

        # Сначала доходы
        self.assertEqual(categories[0], c2)

        # Внутри расходов сортировка по name
        self.assertEqual(categories[1], c3)  # Авто
        self.assertEqual(categories[2], c1)  # Еда
