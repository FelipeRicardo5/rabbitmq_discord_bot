from src.main.rabbitmq_configs.cnsmr_process_tasks import RabbitMQConsumer

"""
Módulo responsável por rodar o conumer.
"""

if __name__ == "__main__":
    try:
        consumer = RabbitMQConsumer()
        consumer.start()
    except KeyboardInterrupt:
        print("Conexão fechada")