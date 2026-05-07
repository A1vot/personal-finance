from django.urls import path
from .views import (
    login_view,
    dashboard_view,
    register_view,
    delete_transaction_view,
)


urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path(
        "transactions/delete/<int:transaction_id>/",
        delete_transaction_view,
        name="delete_transaction",
    ),
]
