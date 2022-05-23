import uuid
import pika

from metro_request_enum import MetroRequest


class MetroClient:
    def __init__(self):
        self.corr_id = None
        self.response = None
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='metro_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode('utf-8')

    def add_line(self, color: str):
        self.call([MetroRequest.ADD_LINE.value, [color]])

    def add_station(self, name: str, line_id: int, open: str, close: str):
        self.call([MetroRequest.ADD_STATION.value, [name, line_id, open, close]])

    def delete_station(self, id: int):
        self.call([MetroRequest.DELETE_STATION.value, [id]])

    def get_line_stations_list(self, id: int):
        return eval(self.call([MetroRequest.LIST_OF_LINE_STATIONS.value, [id]]))

    def get_lines_list(self):
        return eval(self.call([MetroRequest.LIST_OF_LINES.value, []]))

    def get_stations_list(self):
        return eval(self.call([MetroRequest.LIST_OF_STATIONS.value, []]))

    def reset_db(self):
        self.call([MetroRequest.RESET_DB.value, []])
