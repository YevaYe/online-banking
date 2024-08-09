from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from bank.models import User, Transaction, Account, Category, Country


# admin.site.register(User)
@admin.register(User)
class ClientAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "birthday",
        "country",
        "user_type",
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("birthday", "country", "user_type")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "birthday",
                        "country",
                        "user_type",
                    )
                },
            ),
        )
    )


# admin.site.register(Transaction)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ("account_from", "account_to", "date", "category", "amount")
    list_filter = ("date",)


admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Country)
