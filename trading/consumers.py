import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .external_service import ExternalWebSocketService

class TradingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Add to the trading group
        async_to_sync(self.channel_layer.group_add)(
            "trading",
            self.channel_name
        )
        # Send initial connection status
        service = ExternalWebSocketService.get_instance()
        self.send(json.dumps({
            'type': 'connection_status',
            'is_external_connected': service.is_connected
        }))

    def disconnect(self, close_code):
        # Remove from the trading group
        async_to_sync(self.channel_layer.group_discard)(
            "trading",
            self.channel_name
        )

    def broadcast_message(self, event):
        # Forward the message to the WebSocket
        self.send(text_data=event["message"])

    def connection_status(self, event):
        # Forward connection status to the WebSocket
        self.send(json.dumps({
            'type': 'connection_status',
            'is_external_connected': event["is_external_connected"]
        }))

    def trade_notification(self, event):
        """
        Handler for trade notifications.
        """
        # Forward the message to WebSocket
        self.send(text_data=json.dumps({
            'type': event['message']['type'],
            'data': event['message']['data']
        })) 