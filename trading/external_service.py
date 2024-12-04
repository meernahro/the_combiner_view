import json
import websocket
import threading
import time
from typing import Optional, Callable
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
class ExternalWebSocketService:
    _instance = None
    
    def __init__(self):
        self.external_ws = None
        self.is_connected = False
        self.should_reconnect = True
        self.channel_layer = get_channel_layer()
        
        # Start single reconnection monitor thread
        self.reconnect_thread = threading.Thread(target=self._reconnect_loop)
        self.reconnect_thread.daemon = True
        self.reconnect_thread.start()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def connect_to_external(self):
        environment = os.getenv("ENVIRONMENT")
        external_ws_url = os.getenv("DEV_EXTERNAL_WS_URL") if environment == "development" else os.getenv("EXTERNAL_WS_URL")
        if self.external_ws:
            try:
                self.external_ws.close()
            except:
                pass
        
        try:
            self.external_ws = websocket.WebSocketApp(
                external_ws_url,
                on_open=self.on_external_open,
                on_close=self.on_external_close,
                on_error=self.on_external_error,
                on_message=self.on_external_message
            )
            # Start the external connection in a separate thread
            self.ws_thread = threading.Thread(target=self.external_ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
        except Exception as e:
            print(f"Failed to connect to external server: {e}")
            self.is_connected = False

    def _reconnect_loop(self):
        while self.should_reconnect:
            if not self.is_connected:
                print("Attempting to reconnect to external server...")
                self.connect_to_external()
            time.sleep(5)  # Check connection status every 5 seconds

    def on_external_open(self, ws):
        print("Connected to external server")
        self.is_connected = True
        self.broadcast_connection_status()

    def on_external_close(self, ws, close_status_code, close_msg):
        print(f"External connection closed: {close_msg}")
        self.is_connected = False
        self.broadcast_connection_status()

    def on_external_error(self, ws, error):
        print(f"External connection error: {error}")
        self.is_connected = False
        self.broadcast_connection_status()

    def on_external_message(self, ws, message):
        try:
            print(f"Received message from external server: {message}")
            # Broadcast message to all connected clients
            from .automation_handler import AutomationHandler
            AutomationHandler.process_message(message)
            async_to_sync(self.channel_layer.group_send)(
                "trading",
                {
                    "type": "broadcast_message",
                    "message": message
                }
            )
        except Exception as e:
            print(f"Error handling external message: {e}")

    def broadcast_connection_status(self):
        try:
            async_to_sync(self.channel_layer.group_send)(
                "trading",
                {
                    "type": "connection_status",
                    "is_external_connected": self.is_connected
                }
            )
        except Exception as e:
            print(f"Error broadcasting connection status: {e}") 