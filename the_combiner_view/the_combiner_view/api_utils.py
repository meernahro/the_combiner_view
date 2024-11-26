# api_utils.py
"""
This Django application serves as a centralized interface to combine and manage multiple external APIs:

1. Trading API (port 8082):
   - User management
   - Trading account operations
   - Trade tracking
   - Integration with multiple exchanges:
     * Binance Spot trading
     * MEXC Spot trading

2. Classifier API (port 8083):
   - Token tracking and classification
   - Channel management
   - Exchange configuration
   - Token monitoring

Architecture:
- This file contains utility classes that wrap HTTP calls to the external services
- Each class (TradeExternalApis, ClassifierExternalApis) encapsulates related endpoints
- All API calls return JSON responses as Python dictionaries
- Type hints are used throughout for better code clarity and IDE support

Note: This is part of a larger Django project that combines views from multiple 
microservices into a single interface. The main Django app serves as an aggregator
and UI layer on top of these specialized services.
"""

import requests
from typing import Dict, Any, Optional, List

class TradeExternalApis:
    """
    Utility class to interact with external trading APIs.
    """
    TRADE_BASE_URL = "http://127.0.0.1:8082"


    # Users
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/users/"
        response = requests.post(url, json=user_data, headers=self.headers)
        return response.json()

    def get_users(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/users/"
        params = {"skip": skip, "limit": limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_user(self, username: str) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/users/{username}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def update_user(self, username: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/users/{username}"
        response = requests.put(url, json=user_data, headers=self.headers)
        return response.json()

    # Trading Accounts
    def create_trading_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/accounts/"
        response = requests.post(url, json=account_data, headers=self.headers)
        return response.json()

    def get_user_accounts(self, username: str) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/accounts/user/{username}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_trading_account(self, account_id: int) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/accounts/{account_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def update_trading_account(self, account_id: int, account_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/accounts/{account_id}"
        response = requests.put(url, json=account_data, headers=self.headers)
        return response.json()

    def verify_trading_account(self, account_id: int, verified: bool) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/accounts/{account_id}/verify"
        params = {"verified": verified}
        response = requests.post(url, headers=self.headers, params=params)
        return response.json()

    # Trades
    def get_account_trades(self, account_id: int, skip: int = 0, limit: int = 100,
                           start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/trades/account/{account_id}"
        params = {"skip": skip, "limit": limit, "start_date": start_date, "end_date": end_date}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_user_trades(self, username: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/trades/user/{username}"
        params = {"skip": skip, "limit": limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_account_trade_stats(self, account_id: int, period: str = "all") -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/trades/stats/account/{account_id}"
        params = {"period": period}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    # Binance Spot
    def get_binance_account_info(self, account_id: int) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/binance/spot/account"
        params = {"account_id": account_id}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_binance_balance(self, account_id: int, asset: str) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/binance/spot/balance/{asset}"
        params = {"account_id": account_id}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def create_binance_order(self, account_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/binance/spot/order"
        params = {"account_id": account_id}
        response = requests.post(url, json=order_data, headers=self.headers, params=params)
        return response.json()

    def get_binance_orders(self, account_id: int, symbol: str, status: str = "all", limit: int = 50) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/binance/spot/orders/{symbol}"
        params = {"account_id": account_id, "status": status, "limit": limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    # MEXC Spot
    def get_mexc_account_info(self, account_id: int) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/account"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_mexc_balance(self, account_id: int, asset: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/balance"
        params = {"asset": asset} if asset else {}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def create_mexc_order(self, account_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/order"
        response = requests.post(url, json=order_data, headers=self.headers)
        return response.json()

    def cancel_mexc_order(self, account_id: int, symbol: str, order_id: str) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/order/{symbol}/{order_id}"
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def get_mexc_order_history(self, account_id: int, symbol: Optional[str] = None, limit: int = 500,
                               from_id: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/orders"
        params = {"symbol": symbol, "limit": limit, "from_id": from_id}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_mexc_open_orders(self, account_id: int, symbol: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/open-orders"
        params = {"symbol": symbol} if symbol else {}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_mexc_orderbook(self, account_id: int, symbol: str, limit: int = 100) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/orderbook/{symbol}"
        params = {"limit": limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def test_mexc_order(self, account_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.TRADE_BASE_URL}/mexc/spot/{account_id}/order/test"
        response = requests.post(url, json=order_data, headers=self.headers)
        return response.json()



class ClassifierExternalApis:
    """
    Utility class to interact with the Telegram Token Tracker API.
    """
    CLASSIFIER_BASE_URL = "http://127.0.0.1:8083"

    # Health Check
    def health_check(self) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/health"
        response = requests.get(url)
        return response.json()

    # Channels
    def add_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/channel/"
        response = requests.post(url, json=channel_data)
        return response.json()

    def delete_channel(self, channel_id: int) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/channel/{channel_id}"
        response = requests.delete(url)
        return response.json()

    def get_channel(self, channel_id: int) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/channel/{channel_id}"
        response = requests.get(url)
        return response.json()

    def get_all_channels(self) -> List[Dict[str, Any]]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/channels/"
        response = requests.get(url)
        return response.json()

    # Exchanges
    def add_exchange(self, exchange_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/exchange/"
        response = requests.post(url, json=exchange_data)
        return response.json()

    def delete_exchange(self, exchange_id: int) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/exchange/{exchange_id}"
        response = requests.delete(url)
        return response.json()

    def get_exchange(self, exchange_id: int) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/exchange/{exchange_id}"
        response = requests.get(url)
        return response.json()

    def get_all_exchanges(self) -> List[Dict[str, Any]]:
        url = f"{self.CLASSIFIER_BASE_URL}/config/exchanges/"
        response = requests.get(url)
        return response.json()

    # Tokens
    def get_tokens(self, exchange: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        url = f"{self.CLASSIFIER_BASE_URL}/tokens/"
        params = {"exchange": exchange, "limit": limit}
        response = requests.get(url, params=params)
        return response.json()

    def get_token(self, token_id: int) -> Dict[str, Any]:
        url = f"{self.CLASSIFIER_BASE_URL}/tokens/{token_id}"
        response = requests.get(url)
        return response.json()

    def get_latest_tokens(self, limit: int = 10) -> List[Dict[str, Any]]:
        url = f"{self.CLASSIFIER_BASE_URL}/tokens/latest/"
        params = {"limit": limit}
        response = requests.get(url, params=params)
        return response.json()
