from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    """Форма для создания и редактирования транзакций."""

    class Meta:
        model = Transaction
        fields = ["category", "amount", "date", "description"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date"},
            ),
        }
