import pika
import json

def rabbitmq_callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    formatted = json.loads(msg)
    print(formatted)
    print(type(formatted))
    print(formatted["msg"])
    
class RabbitMQConsumer:
    def __init__(self): 
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "minhaqueue"
        self.__routing_key = "meu.rk"
        self.__channel = self.create_channel()

    def create_channel(self): 
        # enviando os parametros de conexão.
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel() 
        # instancia do objeto de conexão.

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            auto_ack=True,
            queue=self.__queue,
            on_message_callback=rabbitmq_callback
        )

        return channel
    
    def start(self):
        print("Sistema startado pelo rabbitmq!")
        self.__channel.start_consuming()