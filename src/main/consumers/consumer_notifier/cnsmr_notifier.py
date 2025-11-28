import pika
import json
import time
import os
import discord
import asyncio

from src.main.consumers.settings.connection import create_channel
from callback import process_task_callback

"""
Módulo responsável por ser o ator Consumer e Notifier do Discord,
consome qualquer NOTIFICACAO simula o processamento e cria uma notificação.
"""

intents = discord.Intents.default()
client = discord.Client(intents=intents)

class RabbitMQConsumer:
    def __init__(self): 
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "notificacao"
        self.__exchange = "notifications"
        self.__routing_key = "notificacao.*" # generaliza para qualquer tipo de task 
        self.__channel = create_channel(callback=process_task_callback, 
                                        host=self.__host, 
                                        port=self.__port,
                                        username=self.__username,
                                        password=self.__password,
                                        queue=self.__queue,
                                        exchange=self.__exchange,
                                        routing_key=self.__routing_key
                                        )
    
    def start(self):
        print("Sistema startado pelo rabbitmq!")

        self.__channel.start_consuming()

class Discord:
    def __init__(self):
        self.discord_token = ""
        self.channel_name = ""

    async def send_to_discord(self, data):
        channel = discord.utils.get(client.get_all_channels(), name=self.channel_name)
        if channel:
            await channel.send(f"📢 {data['text']}")
        else:
            print("⚠️ Canal não encontrado!")

@client.event 
async def on_read():
    print(f"Bot conectado como {client.user}")
    loop = asyncio.get_event_loop()
    loop.create_task()