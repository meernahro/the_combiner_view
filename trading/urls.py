from django.urls import path
from . import views
from .views import get_exchanges, get_accounts

app_name = 'trading'

urlpatterns = [
    path('accounts/', views.TradingAccountsView.as_view(), name='accounts'),
    path('accounts/<int:account_id>/verify/', views.verify_account, name='verify_account'),
    path('accounts/<int:account_id>/balance/', views.get_account_balance, name='get_account_balance'),
    path('rules/', views.AutomationRuleView.as_view(), name='rules'),
    path('rules/<int:rule_id>/', views.AutomationRuleView.as_view(), name='rule_detail'),
    path('api/exchanges/', get_exchanges, name='get_exchanges'),
    path('api/accounts/', get_accounts, name='get_accounts'),
]