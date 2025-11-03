from src.main.rabbitmq_configs.consumer import RabbitMQConsumer

"""
Módulo responsável por rodar o conumer.
"""

if __name__ == "__main__":
    try:
        consumer = RabbitMQConsumer()
        consumer.start()
    except KeyboardInterrupt:
        print("Conexão fechada")