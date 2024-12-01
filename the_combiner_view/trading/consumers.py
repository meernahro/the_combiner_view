import json
import websocket
import threading
import time
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class TradingConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.external_ws = None
        self.is_external_connected = False
        self.should_reconnect = True
        self.reconnect_thread = None

    def connect(self):
        self.accept()
        self.connect_to_external()

    def disconnect(self, close_code):
        self.should_reconnect = False
        if self.external_ws:
            self.external_ws.close()

    def connect_to_external(self):
        try:
            self.external_ws = websocket.WebSocketApp(
                "ws://127.0.0.1:8766",
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
            self.is_external_connected = False
            self.schedule_reconnect()

    def schedule_reconnect(self):
        if self.should_reconnect and not self.is_external_connected:
            print("Attempting to reconnect to external server...")
            if self.reconnect_thread is None or not self.reconnect_thread.is_alive():
                self.reconnect_thread = threading.Thread(target=self._reconnect_loop)
                self.reconnect_thread.daemon = True
                self.reconnect_thread.start()

    def _reconnect_loop(self):
        while self.should_reconnect and not self.is_external_connected:
            try:
                self.connect_to_external()
                time.sleep(2)  # Wait before retry to avoid hammering the server
            except Exception as e:
                print(f"Reconnection attempt failed: {e}")

    def on_external_open(self, ws):
        print("Connected to external server")
        self.is_external_connected = True
        self.send_connection_status()

    def on_external_close(self, ws, close_status_code, close_msg):
        print(f"External connection closed: {close_msg}")
        self.is_external_connected = False
        self.send_connection_status()
        self.schedule_reconnect()

    def on_external_error(self, ws, error):
        print(f"External connection error: {error}")
        self.is_external_connected = False
        self.send_connection_status()
        self.schedule_reconnect()

    def on_external_message(self, ws, message):
        # Handle messages from external server
        try:
            self.send(text_data=message)
        except Exception as e:
            print(f"Error handling external message: {e}")

    def send_connection_status(self):
        try:
            self.send(json.dumps({
                'type': 'connection_status',
                'is_external_connected': self.is_external_connected
            }))
        except Exception as e:
            print(f"Error sending connection status: {e}") 