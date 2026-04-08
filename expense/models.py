import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    username = models.CharField(null=True,blank=True)
    email = models.EmailField(unique=True, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    profile_photo = models.ImageField(default='default.jpg', upload_to='profile_images')
    category_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

class DefaultCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Expense(models.Model):
    TRANSACTION_MEDIUM = [
        ("UPI", "UPI"),
        ("Credit Card", "Credit Card"),
        ("Net Banking", "Net Banking"),
        ("Cash", "Cash"),
        ("Other", "Other"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10 ,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_medium = models.CharField(choices=TRANSACTION_MEDIUM)
    date = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.amount} : {self.user}"