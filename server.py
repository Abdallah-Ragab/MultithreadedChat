import socket
import logging
from threading import Thread


class Server():

    Clients = []
    host = "127.0.0.1"
    port = 8080
    logger = logging.getLogger()

    def __init__(self, *args, **kwargs):
        self.run()

    def run(self, *args, **kwargs):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind(self.host, self.port)
        self.logger.info("[ + ] Server Started.")
        self.listen_for_connections()

    def listen_for_connections(self):
        while True:
            self.Socket.listen(1)
            connection, address = self.Socket.accept()
            client = Client(
                id = len(self.Clients),
                connection=connection,
                address=address
            )
            self.Clients.append(client)


class Client:

    def __init__(self, id, connection, address, *args, **kwargs):
        pass

class Connection(Thread):

    def __init__(self, client,  *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)