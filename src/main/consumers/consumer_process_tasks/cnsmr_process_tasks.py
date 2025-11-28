import pika
import json
import time
import os

from src.main.consumers.settings.connection import create_channel
from callback import process_task_callback

"""
Módulo responsável por ser o ator Consumer,
consome qualquer TASK simula o processamento e cria uma notificação.
"""
    
class RabbitMQConsumer:
    def __init__(self): 
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "task"
        self.__exchange = "tasks"
        self.__routing_key = "task.*" # generaliza para qualquer tipo de task 
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