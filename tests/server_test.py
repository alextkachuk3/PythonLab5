from test_config import db_host, db_port, db_user, db_password, db_name
from server.metro_server import MetroServer

server = MetroServer(db_host, db_port, db_user, db_password, db_name)
server.run()
