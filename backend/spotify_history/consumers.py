from channels.generic.websocket import WebsocketConsumer
import json
import random
from loguru import logger
class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logger.info(f'Received message: {text_data_json['message']}')
        
        self.send(text_data=json.dumps({
            'message': f'hi mate ({random.randint(1, 10)})'
        }))
