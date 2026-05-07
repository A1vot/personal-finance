from django import forms
from .models import Budget


class BudgetForm(forms.ModelForm):
    """Форма для редактирования месячного бюджета пользователя."""

    class Meta:
        model = Budget
        fields = ["monthly_limit"]
        widgets = {
            "monthly_limit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Введите месячный лимит",
                }
            )
        }
