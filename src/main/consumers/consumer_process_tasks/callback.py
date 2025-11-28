import json
import time

# recebe o corpo vindo do publisher e processa.
def process_task_callback(ch, method, properties, body):

    task = body.decode("utf-8")
    task_formatted = json.loads(task)

    notification = {
        "text": f"Tarefa concluída: {task_formatted['data']}",
        "type": task_formatted["type"]
    }
    print("recebendo mensagem...")
    time.sleep(1)
    print(notification) # mensagem já convertida a objeto python