from django.db import models


class Category(models.Model):
    """Категория доходов или расходов."""

    TYPE_CHOICES = [
        ("income", "Доход"),
        ("expense", "Расход"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Тип",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-type", "name"]  # Доходы → расходы, внутри — по имени

    def __str__(self):
        """Строковое представление категории."""
        return f"{self.name} ({self.get_type_display()})"
