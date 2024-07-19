from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("regular", "Regular User"),
        ("entrepreneur", "Entrepreneur"),
    )

    birthday = models.DateField(blank=True, null=True)
    date_of_joining = models.DateField(auto_now_add=True)  # під час створення юзера
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    # функція вибрати із запропонованого поки вводиш дані
    user_type = models.CharField(max_length=12, choices=USER_TYPE_CHOICES, default="regular")
    service_category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Унікальне related_name
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # Унікальне related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


class Transaction(models.Model):
    account_from = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="account_from")
    account_to = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="account_to")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category_name")

    def clean(self):
        if self.account_from == self.account_to:
            raise ValidationError("Account from and account to shouldn't be the same")
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero")


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = (
        ("expense", "Expense Category"),
        ("income", "Income Category"),
    )

    name = models.CharField(max_length=100)
    type_of_category = models.CharField(max_length=15, choices=CATEGORY_TYPE_CHOICES)


class Country(models.Model):
    name = models.CharField(max_length=100)
    national_currency_name = models.CharField(max_length=50)
    national_currency_symbol = models.CharField(max_length=1)

    def __str__(self):
        return self.name
