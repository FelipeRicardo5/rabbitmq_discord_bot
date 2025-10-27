import pika

def setup_rabbit():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel = connection.channel()

    # Exchange
    channel.exchange_declare(
        exchange="minhaexchange",
        exchange_type="direct",
        durable=True
    )

    # Fila
    channel.queue_declare(
        queue="minhaqueue",
        durable=True
    )

    # Binding
    channel.queue_bind(
        queue="minhaqueue",
        exchange="minhaexchange",
        routing_key="meu.rk" # funciona como uma etiqueta ou filtro 
    )

    connection.close()
