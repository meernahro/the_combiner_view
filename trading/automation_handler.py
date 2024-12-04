import logging
from typing import List, Dict, Any
from .models import AutomationRule

logger = logging.getLogger(__name__)

class AutomationHandler:
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

            rule_exchanges = [x.lower() for x in rule.exchanges]
            print(f"  Rule exchanges: {rule_exchanges}")
            
            matching_tokens = [
                token for token in tokens_data
                if token.get('exchange', '').lower() in rule_exchanges
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
        The rule's exchanges field indicates which exchanges to monitor for listings,
        while the account field specifies where to execute the trades.
        """
        try:
            print("\n    Processing Matching Tokens")
            print(f"    Total matching tokens: {len(matching_tokens)}")
            
            if len(matching_tokens) > 2:
                print(f"    Skipping: Too many tokens ({len(matching_tokens)}). Maximum allowed: 2")
                return
                
            print(f"    Total USDT amount: {rule.amount_usdt}")
            usdt_per_token = rule.amount_usdt / len(matching_tokens)
            print(f"    USDT per token ({rule.amount_usdt} / {len(matching_tokens)}): {usdt_per_token}")
            
            for index, token in enumerate(matching_tokens, 1):
                print(f"\n    Trade Signal {index}/{len(matching_tokens)}:")
                print(f"    - Rule ID: {rule.id}")
                print(f"    - Listing Exchange: {token.get('exchange')}")  # Exchange where listing was detected
                print(f"    - Trading Account: {rule.account}")  # Account to execute trade with
                print(f"    - Token: {token.get('token')}")
                print(f"    - Amount: {usdt_per_token} USDT")

                logger.info(
                    f"Trade Signal {index}/{len(matching_tokens)} - Rule {rule.id}: "
                    f"Token {token.get('token')} listed on {token.get('exchange')}, "
                    f"Trading via account: {rule.account}, "
                    f"Amount: {usdt_per_token} USDT"
                )

        except Exception as e:
            print(f"Error in _handle_matching_tokens: {str(e)}")
            logger.error(f"Error handling matching tokens for rule {rule.id}: {e}", exc_info=True)
        finally:
            print("    Token Processing Complete") 