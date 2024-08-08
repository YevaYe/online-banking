from django import forms
from django.core.exceptions import ValidationError

from .models import Account, Category, Country, generate_unique_account_number


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["number", "account_category"]
        widgets = {
            "number": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(AccountForm, self).__init__(*args, **kwargs)

        # Генеруємо унікальний номер акаунту та встановлюємо його в форму
        if not self.instance.pk:
            self.instance.number = generate_unique_account_number()

        # Якщо користувач не є підприємцем, приховуємо поле account_category
        if self.user.user_type != "entrepreneur":
            # self.fields["account_category"].initial = Category.objects.get_or_create(
            #     name="Transfer"
            # )[0]
            self.fields["account_category"].widget = forms.HiddenInput()

        self.fields["number"].widget.attrs["readonly"] = True

    def save(self, commit=True):
        account = super(AccountForm, self).save(commit=False)
        account.user = self.user
        account.balance = 0
        if commit:
            account.save()
        return account


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type_of_category"]


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["name", "national_currency_name", "national_currency_symbol"]


class TransactionSearchForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="",
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Search by date. Format: DD-MM-YYYY"}
        ),
    )


class MoneyTransferForm(forms.Form):
    sender_account = forms.ModelChoiceField(
        queryset=None, widget=forms.Select(attrs={"placeholder": "Sender Account"})
    )
    recipient_account_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={"placeholder": "Recipient Account Number"}),
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(MoneyTransferForm, self).__init__(*args, **kwargs)
        self.fields["sender_account"].queryset = Account.objects.filter(user=user)

    def clean_recipient_account_number(self):
        account_number = self.cleaned_data.get("recipient_account_number")
        if not account_number.isdigit() or len(account_number) != 16:
            raise ValidationError("Account number must be 16 digits.")
        if not Account.objects.filter(number=account_number).exists():
            raise ValidationError("Account does not exist.")
        return account_number

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        sender_account = cleaned_data.get("sender_account")
        recipient_account_number = cleaned_data.get("recipient_account_number")

        if sender_account and sender_account.number == recipient_account_number:
            raise ValidationError("Cannot transfer money to the same account.")

        return cleaned_data
