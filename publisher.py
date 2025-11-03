import pika
import json
from src.main.setup import setup_rabbit
import time

"""
Módulo responsável por ser o ator Publisher, 
declara o exchange do tipo TOPIC gerenciador de task e remetente de cada task.
"""

class RabbitMQPublisher:
    def __init__(self):
        # dentro do nosso método especial que é instanciado automaticamente.
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "tasks"
        self.__exchange_type = "topic"
        self.__routing_key = ""
        self.__channel = self.create_channel()

    # cria o canal
    def create_channel(self):
        # armazeno e defino os parametros de conexão.
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            ),
        )
        # obj de conexáo.
        conn = pika.BlockingConnection(connection_parameters)

        channel = conn.channel()
        channel.confirm_delivery() # modo de confirmação

        # apartir do canal, declara a exchange
        channel.exchange_declare(
        exchange=self.__exchange,
        exchange_type=self.__exchange_type,     
        durable=True                
        )
        return channel

    def process_tasks(self) -> list:
        tasks = [
            {"type": "relatorio", 
             "data": "Gerar relatório financeiro"},

            {"type": "email", 
             "data": "Enviar email para usuários"},

            {"type": "backup", 
             "data": "Executar backup do banco"},
        ]
        return tasks

    # envia msg
    def send_message(self):
            try:
                tasks = self.process_tasks()
                for task in tasks:
                    print(f"🚶‍♂️‍➡️Enviando TASK, do tipo: {task["type"]}...")
                    time.sleep(1)
                    routing_key = f"task.{task["type"]}"
                    print(f"routing_key: {routing_key}")
                    print(task)
                    self.__channel.basic_publish(
                        exchange=self.__exchange,
                        routing_key=routing_key,
                        body=json.dumps(task), # como nos definimos o body como um dict nos serializamos para um JSON str.
                        properties=pika.BasicProperties(
                            delivery_mode=2
                        ),
                        mandatory=True
                    )
                    print(f"🙋TASK enviada, do tipo: {task["type"]}")
            except Exception as e:
                 print("Mensagem não enviada!")
                 print(e)
        
pub = RabbitMQPublisher() 
pub.send_message()