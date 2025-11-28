import pika 
# from callback import process_task_callback

def create_channel(callback: callable, host, port, username, password, queue, exchange, routing_key): 
        # armazeno e defino os parametros de conexão.
        connection_parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(
                username=username,
                password=password
            )
        )
        # obj de conexáo.
        conn = pika.BlockingConnection(connection_parameters)

        channel = conn.channel()

        channel.queue_declare(
            queue=queue,
            durable=True
        )
        # reforça a bind entre a exchange e a queue
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

        channel.basic_consume(
            queue=queue,
            on_message_callback=callback,
            auto_ack=True,
        )

        return channel