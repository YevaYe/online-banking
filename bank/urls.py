from django.urls import path

from .views import (
    index,
    # AccountListView,
    CategoryListView,
    CountryListView,
    TransactionListView,
    MyBalanceView,
)

app_name = "bank"

urlpatterns = [
    path("", index, name="index"),
    path("my-balance/", MyBalanceView.as_view(), name="my-balance"),
    # path("balance/", AccountListView.as_view(), name="account-list"),
    path("category/", CategoryListView.as_view(), name="category-list"),
    path("country/", CountryListView.as_view(), name="country-list"),
    path("transaction/", TransactionListView.as_view(), name="transaction-list"),
]
