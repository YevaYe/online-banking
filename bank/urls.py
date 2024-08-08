from django.urls import path

from django.contrib.auth import views as auth_views

from .views import (
    index,
    # AccountListView,
    CategoryListView,
    CountryListView,
    TransactionListView,
    MyBalanceView,
    MoneyTransferView,
    AccountCreateView,
    AccountDeleteView,
)

app_name = "bank"

urlpatterns = [
    path("", index, name="index"),
    path("my-balance/", MyBalanceView.as_view(), name="my-balance"),
    path("account/create/", AccountCreateView.as_view(), name="account-create"),
    path(
        "account/<int:pk>/delete/", AccountDeleteView.as_view(), name="account-delete"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("countries/", CountryListView.as_view(), name="country-list"),
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("money-transfer/", MoneyTransferView.as_view(), name="money-transfer"),
]
