import logging
import json
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from the_combiner_view.api_utils import TradeExternalApis
import requests

logger = logging.getLogger(__name__)

class TradingAccountsView(LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()
        self.trade_api = TradeExternalApis()

    def get(self, request):
        context = {}
        try:
            logger.info(f"Fetching trading accounts for user: {request.user.username}")
            
            try:
                user_data = self.trade_api.get_user_accounts(request.user.username)
                logger.info(f"Raw user data response: {user_data}")
                
                if user_data.get('status') == 'success':
                    accounts = user_data.get('accounts', [])
                    logger.info(f"Found {len(accounts)} trading accounts")
                    context['trading_accounts_json'] = json.dumps(accounts)
                else:
                    logger.warning(f"Failed to get user data: {user_data}")
                    context['error'] = "Failed to fetch trading accounts"
                    context['trading_accounts_json'] = '[]'
                    
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Connection error to trading API: {str(e)}")
                context['error'] = "Unable to connect to trading service. Please ensure the trading service is running."
                context['trading_accounts_json'] = '[]'
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error to trading API: {str(e)}")
                context['error'] = "Error communicating with trading service"
                context['trading_accounts_json'] = '[]'
                
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            context['error'] = "An unexpected error occurred"
            context['trading_accounts_json'] = '[]'
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': 'error' not in context,
                'accounts': json.loads(context.get('trading_accounts_json', '[]')),
                'error': context.get('error')
            })
            
        return render(request, 'trading/accounts.html', context)
