import pika
import json
import time
import os

"""
Módulo responsável por ser o ator Consumer,
consome qualquer TASK simula o processamento e cria uma notificação.
"""
# recebe o corpo vindo do publisher e processa.
def rabbitmq_callback(ch, method, properties, body):

    msg = body.decode("utf-8")
    formatted = json.loads(msg)
    print("recebendo mensagem...")
    time.sleep(1)
    print(formatted) # mensagem já convertida a objeto python

    
class RabbitMQConsumer:
    def __init__(self): 
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "task"
        self.__exchange = "tasks"
        self.__routing_key = "task.*"
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
            on_message_callback=rabbitmq_callback,
            auto_ack=True,
        )

        return channel
    
    def start(self):
        print("Sistema startado pelo rabbitmq!")
        self.__channel.start_consuming()