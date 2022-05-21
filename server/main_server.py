from config import db_host, db_port, db_user, db_password, db_name
from server.metro_server import MetroServer

if __name__ == '__main__':
    server = MetroServer(db_host, db_port, db_user, db_password, db_name)
    server.run()
