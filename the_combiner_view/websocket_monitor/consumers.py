from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TokenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("token_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("token_updates", self.channel_name)

    async def token_update(self, event):
        # Immediately send token updates to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'tokens',
            'data': event['data']
        })) 