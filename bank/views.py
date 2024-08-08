from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView

from bank.forms import (
    CountryForm,
    CategoryForm,
    AccountForm,
    TransactionSearchForm,
    MoneyTransferForm,
)
from bank.models import Account, Category, Country, Transaction, User


@login_required
def index(request):
    """View function for the home page of the site."""

    num_general_users = User.objects.filter(user_type="regular").count()
    num_entrepreneurs = User.objects.filter(user_type="entrepreneur").count()
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
    context_object_name = "category_list"
    pagination = 5


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
    context_object_name = "country_list"
    paginate_by = 5


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
    template_name = "bank/transaction_list.html"
    context_object_name = "transaction_list"
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        date = self.request.GET.get("date", "")

        context["search_form"] = TransactionSearchForm(initial={"date": date})
        return context

    def get_queryset(self):
        user = self.request.user
        user_accounts = user.accounts.all()
        queryset = Transaction.objects.filter(
            Q(account_from__in=user_accounts) | Q(account_to__in=user_accounts)
        )
        form = TransactionSearchForm(self.request.GET)
        if form.is_valid():
            date = form.cleaned_data["date"]
            if date:
                queryset = queryset.filter(date=date)
        return queryset


class MoneyTransferView(LoginRequiredMixin, View):
    form_class = MoneyTransferForm
    template_name = "bank/money_transfer.html"
    success_url = reverse_lazy("bank:transaction-list")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            recipient_account_number = form.cleaned_data["recipient_account_number"]
            amount = form.cleaned_data["amount"]

            try:
                with transaction.atomic():
                    sender_account = request.user.accounts.first()
                    recipient_account = Account.objects.get(
                        number=recipient_account_number
                    )

                    if sender_account.balance < amount:
                        raise ValidationError("Insufficient funds.")

                    sender_account.balance -= amount
                    sender_account.save()

                    recipient_account.balance += amount
                    recipient_account.save()

                    category = (
                        recipient_account.account_category
                        or Category.objects.get_or_create(name="Transfer")[0]
                    )

                    Transaction.objects.create(
                        account_from=sender_account,
                        account_to=recipient_account,
                        amount=amount,
                        category=category,
                    )

                return redirect(self.success_url)
            except ValidationError as e:
                form.add_error(None, e.message)
            except Account.DoesNotExist:
                form.add_error(
                    "recipient_account_number", "Recipient account does not exist."
                )

        return render(request, self.template_name, {"form": form})
