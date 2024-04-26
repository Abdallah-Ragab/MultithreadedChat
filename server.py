import socket
import logging
from threading import Thread


class Server(Thread):

    host = "127.0.0.1"
    port = 99
    logger = logging.getLogger()
    logger.info = print

    def __init__(self, *args, **kwargs):
        self.clients = []
        super(Server, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.host, self.port))
        self.logger.info("[ + ] Server Started.")
        self.listen_for_connections()

    def listen_for_connections(self):
        while True:
            self.Socket.listen(1)
            connection, address = self.Socket.accept()
            client = Connection(
                id=len(self.clients),
                connection=connection,
                address=address,
                server=self,
            )
            self.clients.append(client)


class Connection(Thread):

    def __init__(self, id, connection, address, server, *args, **kwargs):
        self.id = id
        self.connection = connection
        self.address = address
        self.server = server
        super(Connection, self).__init__(*args, **kwargs)

    def run(self) -> None:
        self.listen_for_messages()

    def listen_for_messages(self):
        while True:
            try:
                raw_message = self.connection.recv().decode()
            except:
                # disconnected
                break
