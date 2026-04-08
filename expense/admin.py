from django.contrib import admin
from .models import User, Profile, Category, Expense, DefaultCategory
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(DefaultCategory)