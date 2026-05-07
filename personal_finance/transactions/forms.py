from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    """Форма для создания и редактирования транзакций."""

    class Meta:
        model = Transaction
        fields = ["category", "amount", "date", "description"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
