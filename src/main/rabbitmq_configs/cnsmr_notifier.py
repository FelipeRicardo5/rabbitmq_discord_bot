import pika
import json
import time
import os
import discord
import asyncio

"""
Módulo responsável por ser o ator Consumer e Notifier do Discord,
consome qualquer NOTIFICACAO simula o processamento e cria uma notificação.
"""

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# recebe o corpo vindo do publisher e processa.
def process_task_callback(ch, method, properties, body):

    task = body.decode("utf-8")
    task_formatted = json.loads(task)

    notification = {
        "text": f"Tarefa concluída: {task_formatted['data']}",
        "type": task_formatted["type"]
    }
    print("recebendo mensagem...")
    time.sleep(1)
    print(notification) # mensagem já convertida a objeto python

    
class RabbitMQConsumer:
    def __init__(self): 
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "notificacao"
        self.__exchange = "notifications"
        self.__routing_key = "notificacao.*" # generaliza para qualquer tipo de task 
        self.__channel = self.create_channel()

    def create_channel(self): 
        # armazeno e defino os parametros de conexão.
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )
        # obj de conexáo.
        conn = pika.BlockingConnection(connection_parameters)

        channel = conn.channel()

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        # reforça a bind entre a exchange e a queue
        channel.queue_bind(queue=self.__queue, exchange=self.__exchange, routing_key=self.__routing_key)

        channel.basic_consume(
            queue=self.__queue,
            on_message_callback=process_task_callback,
            auto_ack=True,
        )

        return channel
    
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