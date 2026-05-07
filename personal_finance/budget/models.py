from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    """Модель месячного бюджета, привязанная к конкретному пользователю."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Месячный лимит",
    )

    class Meta:
        verbose_name = "Бюджет"
        verbose_name_plural = "Бюджет"
        ordering = ["user", "monthly_limit"]

    def __str__(self):
        """Строковое представление бюджета."""
        return f"Бюджет {self.user.username}"
