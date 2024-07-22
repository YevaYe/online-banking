from django.contrib import admin

from bank.models import User, Transaction, Account, Category, Country

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Country)
