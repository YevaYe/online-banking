from django.urls import path

from bank.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "bank"
