import socket
import logging
from threading import Thread
from message import Message


class Server(Thread):

    host = "127.0.0.1"
    port = 99
    logger = logging.getLogger()
    logger.info = print

    def __init__(self, *args, **kwargs):
        self.clients = {}
        super(Server, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.host, self.port))
        self.logger.info("[ + ] Server Started.")
        self.listen_for_connections()

    def add_client(self, client, connection, address):
        id = max(self.clients.keys()) + 1 if self.clients else 0
        client = Connection(
            id=id,
            connection=connection,
            address=address,
            server=self,
        )
        self.clients[id] = client

    def listen_for_connections(self):
        while True:
            self.Socket.listen(1)
            connection, address = self.Socket.accept()
            self.add_client(connection, address)


    def send_to_all_clients(self, message: Message):
        for client in self.clients.values():
            client.connection.sendall(str(message).encode())

    def send_to_client(self, client_id: int, message: Message):
        client = self.clients[client_id]
        client.connection.sendall(str(message).encode())

    def announce(self, message: str):
        formatted_message = f'Server: {message}'
        message = Message.from_content("announcement", formatted_message)
        self.send_to_all_clients(message)

    def kick(self, client_id: int):
        client = self.clients[client_id]
        client.connection.close()
        self.clients.remove(client)
        self.announce(f'{client.id} has been kicked.')

    def shutdown(self):
        for client in self.clients:
            client.connection.close()
        self.Socket.close()
        self.logger.info("[ ! ] Server Stopped.")


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
                self.disconnect()

    def disconnect(self):
        self.connection.close()
        self.server.clients.remove(self)
        self.server.announce(f'{self.id} has disconnected.')