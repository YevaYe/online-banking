import random

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def generate_unique_account_number():
    while True:
        number = random.randint(1111_1111_1111_1111, 9999_9999_9999_9999)
        if not Account.objects.filter(number=number).exists():
            return number


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("regular", "Regular User"),
        ("entrepreneur", "Entrepreneur"),
    )

    birthday = models.DateField(blank=True, null=True)
    date_of_joining = models.DateField(auto_now_add=True)  # під час створення юзера
    country = models.ForeignKey("Country", on_delete=models.SET_NULL, null=True)
    # функція вибрати із запропонованого поки вводиш дані
    user_type = models.CharField(
        max_length=12, choices=USER_TYPE_CHOICES, default="regular"
    )
    # service_category = models.ForeignKey("Category", on_delete=models.SET_NULL, blank=True, null=True)

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

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Transaction(models.Model):
    account_from = models.ForeignKey(
        "Account", on_delete=models.SET_NULL, related_name="account_from", null=True
    )
    account_to = models.ForeignKey(
        "Account", on_delete=models.SET_NULL, related_name="account_to", null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, related_name="category_name", null=True
    )

    def clean(self):
        if self.account_from == self.account_to:
            raise ValidationError("Account from and account to shouldn't be the same")
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero")

    class Meta:
        ordering = ["-id"]


class Account(models.Model):
    number = models.IntegerField(
        unique=True,
        validators=[
            MinValueValidator(1111_1111_1111_1111),
            MaxValueValidator(9999_9999_9999_9999),
        ],
        blank=True,
        null=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    account_category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = generate_unique_account_number()
        if self.user.user_type != "entrepreneur" and self.account_category is not None:
            raise ValidationError("Only entrepreneurs can have account categories.")
        if self._state.adding and self.balance is None:
            self.balance = 0
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} (owner: {self.user.username})"


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = (
        ("expense", "Expense Category"),
        ("income", "Income Category"),
    )

    name = models.CharField(max_length=100)
    type_of_category = models.CharField(max_length=15, choices=CATEGORY_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name}"


class Country(models.Model):
    name = models.CharField(max_length=100)
    national_currency_name = models.CharField(max_length=50)
    national_currency_symbol = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.name} ({self.national_currency_name}, {self.national_currency_symbol})"
