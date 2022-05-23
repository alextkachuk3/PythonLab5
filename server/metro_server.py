import pika

from metro_request_enum import MetroRequest
from server.metro import Metro


class MetroServer:
    def __init__(self, db_host, db_port, db_user, db_password, db_name):
        self.metro = Metro(db_host, db_port, db_user, db_password, db_name)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='metro_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='metro_queue', on_message_callback=self.on_request)

    def on_request(self, ch, method, props, body):
        print(body.decode('utf-8'))

        request = eval(body.decode('utf-8'))

        request_enum = MetroRequest(request[0])
        request_data = request[1]

        response = ''

        match request_enum:
            case MetroRequest.ADD_LINE:
                self.metro.add_line(request_data[0])
            case MetroRequest.ADD_STATION:
                self.metro.add_station(request_data[0], request_data[1], request_data[2], request_data[3])
            case MetroRequest.DELETE_STATION:
                self.metro.delete_station(request_data[0])
            case MetroRequest.LIST_OF_LINE_STATIONS:
                response = self.metro.get_line_stations(request_data[0])
            case MetroRequest.LIST_OF_LINES:
                response = self.metro.get_lines_list()
            case MetroRequest.LIST_OF_STATIONS:
                response = self.metro.get_stations_list()
            case MetroRequest.RESET_DB:
                self.metro.connection.cursor().execute("DROP TABLE metro_lines, metro_stations")
                self.metro.connection.commit()
                self.metro.init_tables()

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print("Awaiting requests")
        self.channel.start_consuming()
