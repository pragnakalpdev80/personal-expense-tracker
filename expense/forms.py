import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Profile, Category, Expense


User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.is_active = False 
    #     if commit:
    #         user.save()
    #     return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['profile_photo']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'transaction_medium', 'date', 'notes']
        widgets = {
            'date': DateInput()
        }

    def __init__(self, user, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(Q(user=user) | Q(is_default=True))

    def clean(self):
        cleaned_data = super().clean()  
        amount = cleaned_data.get('amount')
        print(amount)
        date = cleaned_data.get('date')

        if amount == None:
            raise forms.ValidationError("Please enter a valid amount.")

        if amount <= 0:
            raise forms.ValidationError("Amount must be postive.")
        
        if amount > 9999999999:
            raise forms.ValidationError("Please enter amount less than 9999999999")
        
        if date > datetime.date.today():
            raise forms.ValidationError("Date cannot be future date.")
        
        return cleaned_data