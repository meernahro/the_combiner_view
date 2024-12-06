import logging
from typing import List, Dict, Any
from .models import AutomationRule
from the_combiner_view.api_utils import TradeExternalApis
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)
trade_api = TradeExternalApis()

class AutomationHandler:
    @staticmethod
    def _normalize_exchange_name(exchange: str) -> str:
        """
        Normalize exchange names for comparison by removing spaces and special characters
        and converting to lowercase
        """
        return ''.join(e for e in exchange.lower() if e.isalnum())

    @staticmethod
    def _exchanges_match(rule_exchanges: List[str], token_exchange: str) -> bool:
        """
        Check if token exchange matches any of the rule exchanges using normalized names
        """
        if not token_exchange:
            return False
            
        normalized_token_exchange = AutomationHandler._normalize_exchange_name(token_exchange)
        
        print(f"      Comparing exchanges:")
        print(f"      - Token exchange: {token_exchange} -> {normalized_token_exchange}")
        print(f"      - Rule exchanges: {rule_exchanges}")
        
        for rule_exchange in rule_exchanges:
            normalized_rule = AutomationHandler._normalize_exchange_name(rule_exchange)
            print(f"      - Comparing with: {rule_exchange} -> {normalized_rule}")
            
            # Basic match
            if normalized_rule == normalized_token_exchange:
                print(f"      ✓ Exact match")
                return True
                
            # Coinbase special handling
            if 'coinbase' in normalized_token_exchange and 'coinbase' in normalized_rule:
                print(f"      ✓ Coinbase match")
                return True
                
        print(f"      × No match found")
        return False

    @staticmethod
    def _execute_trade(account_id: int, token: str, amount: float, account_info: Dict[str, Any]) -> None:
        """
        Execute trade for a single token
        """
        try:
            symbol = f"{token}USDT"
            print(f"\n      Executing trade for {symbol}")
            print(f"      Account: {account_info['name']} ({account_info['exchange']})")
            print(f"      Amount: {amount} USDT")

            order_data = {
                "symbol": symbol,
                "side": "BUY",
                "type": "MARKET",
                "quote_order_qty": amount
            }

            if account_info['exchange'].lower() == 'mexc':
                print(f"      Sending MEXC market order: {order_data}")
                response = trade_api.create_mexc_order(account_id, order_data)
                print(f"      MEXC Order Response: {response}")
                
                # Emit WebSocket message for trade notification
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "trading",
                    {
                        "type": "trade_notification",
                        "message": {
                            "type": "mexc_trade",
                            "data": response
                        }
                    }
                )
            else:
                print(f"      Unsupported exchange: {account_info['exchange']}")

        except Exception as e:
            print(f"      Error executing trade: {str(e)}")
            logger.error(f"Trade execution error: {str(e)}", exc_info=True)

    @staticmethod
    def _evaluate_rule(rule: AutomationRule, tokens_data: List[Dict[str, Any]]) -> None:
        """
        Evaluate a single rule against token data.
        """
        try:
            print("\n  Evaluating Rule Criteria")
            
            token_market = tokens_data[0].get('market', '').lower()
            print(f"  Token market: {token_market}, Rule market: {rule.market_type}")
            
            if rule.market_type != 'both' and rule.market_type != token_market:
                print("  Market type mismatch - skipping rule")
                return

            # Check if any token matches rule exchanges
            matching_tokens = [
                token for token in tokens_data
                if AutomationHandler._exchanges_match(rule.exchanges, token.get('exchange', ''))
            ]

            if matching_tokens:
                print(f"  Found {len(matching_tokens)} matching tokens")
                print(f"  Matching tokens: {matching_tokens}")
                AutomationHandler._handle_matching_tokens(rule, matching_tokens)
            else:
                print("  No matching tokens found for this rule")

        except Exception as e:
            print(f"Error in _evaluate_rule: {str(e)}")
            logger.error(f"Error evaluating rule {rule.id}: {e}", exc_info=True)

    @staticmethod
    def _handle_matching_tokens(rule: AutomationRule, matching_tokens: List[Dict[str, Any]]) -> None:
        """
        Handle tokens that match rule criteria. Limited to maximum 2 tokens.
        Execute trades through the appropriate exchange API.
        """
        try:
            print("\n    Processing Matching Tokens")
            print(f"    Total matching tokens: {len(matching_tokens)}")
            
            if len(matching_tokens) > 2:
                print(f"    Skipping: Too many tokens ({len(matching_tokens)}). Maximum allowed: 2")
                return

            # Get account information
            try:
                account_id = int(rule.account)
                account_info = trade_api.get_trading_account(account_id)
                
                if not account_info.get('id'):
                    print(f"    Error: Could not fetch account info for ID {account_id}")
                    return

                print(f"    Account Info: {account_info}")
                
                # Calculate USDT amount per token
                usdt_per_token = rule.amount_usdt / len(matching_tokens)
                print(f"    USDT per token ({rule.amount_usdt} / {len(matching_tokens)}): {usdt_per_token}")
                
                # Process each token sequentially
                for index, token in enumerate(matching_tokens, 1):
                    print(f"\n    Processing Trade {index}/{len(matching_tokens)}:")
                    print(f"    - Token: {token.get('token')}")
                    print(f"    - Listing Exchange: {token.get('exchange')}")
                    print(f"    - Trading Account: {account_info['name']} ({account_info['exchange']})")
                    print(f"    - Amount: {usdt_per_token} USDT")

                    # Execute the trade
                    AutomationHandler._execute_trade(
                        account_id=account_id,
                        token=token.get('token'),
                        amount=usdt_per_token,
                        account_info=account_info
                    )

            except ValueError as e:
                print(f"    Error: Invalid account ID format: {rule.account}")
                logger.error(f"Invalid account ID format: {rule.account}")
                return

        except Exception as e:
            print(f"Error in _handle_matching_tokens: {str(e)}")
            logger.error(f"Error handling matching tokens for rule {rule.id}: {e}", exc_info=True)
        finally:
            print("    Token Processing Complete")

    @staticmethod
    def process_message(message: Dict[str, Any]) -> None:
        """
        Process incoming websocket message and trigger automation rules if applicable.
        """
        try:
            print("\n=== Starting Message Processing ===")
            print(f"Received message: {message}")

            if not isinstance(message, dict):
                print("Converting string message to dict...")
                message = eval(message)
                
            if message.get('type') != 'tokens':
                print(f"Skipping message of type: {message.get('type')} (not 'tokens')")
                return

            tokens_data = message.get('data', [])
            if not tokens_data:
                print("No token data found in message")
                return

            print(f"Processing tokens data: {tokens_data}")
            AutomationHandler._process_tokens(tokens_data)

        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            logger.error(f"Error processing automation message: {e}", exc_info=True)
        finally:
            print("=== Message Processing Complete ===\n")

    @staticmethod
    def _process_tokens(tokens_data: List[Dict[str, Any]]) -> None:
        """
        Process tokens against active automation rules.
        """
        try:
            print("\n--- Starting Token Processing ---")
            
            active_rules = AutomationRule.objects.filter(status='enabled')
            print(f"Found {active_rules.count()} active rules")
            
            for rule in active_rules:
                print(f"\nEvaluating Rule ID: {rule.id}")
                print(f"Rule details: Market Type: {rule.market_type}, "
                      f"Exchanges: {rule.exchanges}, Amount: {rule.amount_usdt} USDT")
                AutomationHandler._evaluate_rule(rule, tokens_data)

        except Exception as e:
            print(f"Error in _process_tokens: {str(e)}")
            logger.error(f"Error processing tokens for automation: {e}", exc_info=True)
        finally:
            print("--- Token Processing Complete ---\n")
  