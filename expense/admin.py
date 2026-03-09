from django.contrib import admin
from .models import User, Profile, Category, Expense
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Expense)