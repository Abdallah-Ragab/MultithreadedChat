import socket
import logging
import random
from threading import Thread
from message import Message
from admin_app import LogsWidgetHandler



class Server(Thread):

    host = "127.0.0.1"
    port = 99
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    # display logs in console

    def __init__(self,  onmessage=None, onclientadd=None, onclientremove=None, *args, **kwargs):
        self.clients = {}
        self.onmessage = onmessage
        self.onclientadd = onclientadd
        self.onclientremove = onclientremove

        if 'log_handler' in kwargs:
            self.logger.addHandler(kwargs['log_handler'])
            del kwargs['log_handler']

        super(Server, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.host, self.port))
        self.logger.info("[ + ] Server Started.")
        self.logger.info(f"[ + ] Listening on {self.host}:{self.port}")
        self.listen_for_connections()

    def add_client(self, connection, address):
        id = random.randint(0, 10000)
        client = Connection(
            id=id,
            connection=connection,
            address=address,
            server=self,
        )
        self.clients[id] = client
        client.start()
        if self.onclientadd:
            self.onclientadd(client)
        self.logger.info(f"[ i ] user with id #{client.id} has joined.")

    def remove_client(self, client_id: int):
        print("removing client")
        client = self.clients[int(client_id)]
        self.clients.pop(int(client_id))
        if self.onclientremove:
            self.onclientremove(client)

    def listen_for_connections(self):
        while True:
            try:
                self.Socket.listen(1)
                connection, address = self.Socket.accept()
                self.add_client(connection, address)
            except:
                break

    def send_to_all_clients(self, message: Message):
        for client in self.clients.values():
            client.connection.sendall(str(message).encode())
        if self.onmessage:
            self.onmessage(message)
        self.logger.info(f"[ i ] [sent] [all] [{message.type}] {message.display}")

    def send_to_client(self, client_id: int, message: Message):
        client = self.clients[int(client_id)]
        client.connection.sendall(str(message).encode())
        self.logger.info(
            f"[ i ] [sent] [{client.user_identifier}][{message.type}] {message.display}"
        )

    def announce(self, message: str):
        message = Message(msg_type="announcement", content=message, source="Server")
        self.send_to_all_clients(message)

    def send(self, message: str):
        message = Message(msg_type="message", content=message, source="Admin")
        self.send_to_all_clients(message)

    def kick(self, client_id: int):
        client = self.clients[int(client_id)]
        self.announce(f"{client.user_identifier} has been kicked.")
        self.logger.info(f"[ + ] {client.user_identifier} has been kicked.")
        client.disconnect()
        client.destroy()



    def shutdown(self):
        self.announce("Server is shutting down.")
        for client in self.clients.values():
            client.connection.close()
        self.Socket.close()
        self.logger.info("[ ! ] Server Stopped.")


class Connection(Thread):

    def __init__(self, id, connection, address, server, *args, **kwargs):
        self.id = id
        self.connection = connection
        self.address = address
        self.server = server
        self.username = "Anonymous"
        super(Connection, self).__init__(*args, **kwargs)
    @property
    def user_identifier(self):
        return f"{self.username}[{self.id}]"

    def run(self):
        self.listen_for_messages()

    def listen_for_messages(self):
        while True:
            try:
                msg_string = self.connection.recv(1024).decode()
                message = Message(string=msg_string)
                self.handle_message(message)
            except:
                # disconnected
                break

    def handle_message(self, message: Message):
        self.server.logger.info(f"[ + ] [received] [{message.type}] {message.display}")
        if message.type == "message":
            message.source = self.user_identifier
            self.server.send_to_all_clients(message)
        if message.type == "handshake":
            self.username = message.content
            self.server.announce(f"{self.username} has joined. Welcome!")
        if message.type == "disconnect":
            self.disconnect()

    def disconnect(self):
        self.server.announce(f"{self.user_identifier} has disconnected.")
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()
        self.server.remove_client(self.id)

    def destroy(self):
        self._is_running = False