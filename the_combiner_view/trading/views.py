import logging
import json
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from the_combiner_view.api_utils import TradeExternalApis
import requests
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

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

@login_required
@require_http_methods(["POST"])
def verify_account(request, account_id):
    try:
        data = json.loads(request.body)
        verified = data.get('verified', False)
        
        logger.info(f"Verifying account {account_id} with status {verified}")
        
        trade_api = TradeExternalApis()
        response = trade_api.verify_trading_account(account_id, verified)
        
        logger.info(f"API Response: {response}")
        
        if response.get('status') in ['active', 'inactive', 'failed_verification']:
            return JsonResponse({
                'success': True,
                'account': response,
                'status': response['status']
            })
        else:
            logger.warning(f"Unexpected response format: {response}")
            return JsonResponse({
                'success': False,
                'error': 'Unexpected response from trading service'
            }, status=400)
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        logger.error(f"Error verifying account {account_id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
