from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    date = models.DateField(
        verbose_name='Дата'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date']

    def __str__(self):
        return f"{self.category.name}: {self.amount} от {self.date}"
