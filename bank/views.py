import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from bank.forms import CountryForm, CategoryForm, AccountForm
from bank.models import Account, Category, Country, Transaction, Client


@login_required
def index(request):
    """View function for the home page of the site."""

    num_general_users = Client.objects.filter(user_type="regular").count()
    num_entrepreneurs = Client.objects.filter(user_type="entrepreneur").count()
    num_accounts = Account.objects.count()
    num_transactions = Transaction.objects.count()
    num_categories = Category.objects.count()
    num_countries = Country.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_general_users": num_general_users,
        "num_entrepreneurs": num_entrepreneurs,
        "num_accounts": num_accounts,
        "num_transactions": num_transactions,
        "num_categories": num_categories,
        "num_countries": num_countries,
        "num_visits": num_visits + 1,
    }

    return render(request, "bank/index.html", context=context)


# class AdminRequiredMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if hasattr(self, "request"):
            return self.request.user.is_superuser
        return False


# class AccountListView(LoginRequiredMixin, generic.ListView):
#     model = Account
#     context_object_name = "account-list"
#     template_name = "bank/account_list.html"
#     paginate_by = 5


class MyBalanceView(LoginRequiredMixin, TemplateView):
    template_name = "bank/my_balance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Account.objects.filter(user=user)
        total_balance = sum(account.balance for account in accounts)
        context["total_balance"] = total_balance
        context["accounts"] = accounts
        return context


class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    model = Account
    context_object_name = "account"


class AccountCreateView(LoginRequiredMixin, generic.CreateView):
    model = Account
    form_class = AccountForm
    template_name = "bank/account_form.html"
    success_url = reverse_lazy("bank:my-balance")


# class AccountUpdateView(LoginRequiredMixin, generic.UpdateView):
#     model = Account
#     form_class = AccountForm
#     template_name = "bank/account_form.html"
#     success_url = reverse_lazy("bank:account-list")


class AccountDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Account
    template_name = "bank/account_confirm_delete.html"
    success_url = reverse_lazy("bank:my-balance")


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = "bank/category_list.html"
    context_object_name = "category-list"
    pagination = 10


class CategoryCreateView(AdminRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "bank/category_form.html"
    success_url = reverse_lazy("bank:category-list")


class CategoryUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "bank/category_form.html"
    success_url = reverse_lazy("bank:category-list")


class CategoryDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Category
    template_name = "bank/category_confirm_delete.html"
    success_url = reverse_lazy("bank:category-list")


class CountryListView(LoginRequiredMixin, generic.ListView):
    model = Country
    template_name = "bank/country_list.html"
    context_object_name = "country-list"
    paginate_by = 10


class CountryCreateView(AdminRequiredMixin, generic.CreateView):
    model = Country
    form_class = CountryForm
    template_name = "bank/country_form.html"
    success_url = reverse_lazy("bank:country-list")


class CountryUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Country
    form_class = CountryForm
    template_name = "bank/country_form.html"
    success_url = reverse_lazy("bank:country-list")


class CountryDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Country
    template_name = "bank/country_confirm_delete.html"
    success_url = reverse_lazy("bank:country-list")


class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = "bank/transaction-list.html"
    context_object_name = "transaction-list"
    paginate_by = 15
