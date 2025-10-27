import pika
import json
from src.main.setup import setup_rabbit

class RabbitMQPublisher:
    def __init__(self):
        # dentro do nosso método especial que é instanciado juntamente a classe
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "minhaexchange"
        self.__routing_key = "meu.rk"
        self.__channel = self.create_channel()


    def create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            ),
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        
        channel.exchange_declare(
        exchange="minhaexchange",
        exchange_type="direct",     
        durable=True                
    )

        channel.confirm_delivery()

        return channel

    def send_message(self, body: dict):
        try:
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=json.dumps(body), # Ou seja, como nos definimos o body como um dict nos serializamos para um JSON str.
                properties=pika.BasicProperties(
                    delivery_mode=2
                ),
                mandatory=True
            )
        except: 
            print("messagem perdida!")
        

        

rabbt = RabbitMQPublisher() 
rabbt.send_message({"msg": "vindo do publisher"})