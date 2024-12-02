from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('accounts/', views.TradingAccountsView.as_view(), name='accounts'),
    path('accounts/<int:account_id>/verify/', views.verify_account, name='verify_account'),
    path('accounts/<int:account_id>/balance/', views.get_account_balance, name='get_account_balance'),
]