from django.db import models

class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
        )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name='Тип',
        )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
