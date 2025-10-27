import pika
import json

class RabbitMQPublisher:
    def __init__(self):
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "minhaexchange"
        self.__routing_key = "teste"
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
        channel.confirm_delivery()
        return channel

    def send_message(self, body: dict):
        try:
            confirmado = self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=json.dumps(body), # Ou seja, como nos definimos o body como um dict nos serializamos para um JSON str.
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

            if confirmado:
                print("mensgem enviada!")
            else:
                print("mensagem não enviada")

        except: 
            print("messagem perdida!")
        

        

rabbt = RabbitMQPublisher() 
rabbt.send_message({"msg": "vindo do publisher"})