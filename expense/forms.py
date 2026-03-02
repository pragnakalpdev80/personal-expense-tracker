from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

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

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']