from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['monthly_limit']
        widgets = {
            'monthly_limit': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Введите месячный лимит'
            })
        }
