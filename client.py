import logging
import socket
from message import Message


class Client:

    default_server_host = "127.0.0.1"
    default_server_port = 99
    messages = []

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def __init__(self, username="Anonymous", onmessage=None, *args, **kwargs):
        self.username = username
        self.onmessage = onmessage

    def connect(self, ip=None, port=None):
        ip = ip or self.default_server_host
        port = port or self.default_server_port

        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.connect((ip, port))
        self.logger.info(f"[ + ] Connected to server {ip}:{port}")
        self.logger.info("[ i ] Listening for messages.")

        self.send(self.username, msg_type="handshake")

        self.listen_for_messages()

    def send(self, message, msg_type="message"):
        msg = Message(msg_type=msg_type, content=message, source=self.username)
        encoded_msg = str(msg).encode()
        if msg_type == "handshake":
            self.logger.info(f"[ + ] Set username: {message}")
        else:
            self.logger.info(f"[ + ] Sent message: {message}")
        self.Socket.sendall(encoded_msg)

    def listen_for_messages(self):
        while True:
            try:
                raw_message = self.Socket.recv(1024).decode()
                message = Message(string=raw_message)
                if self.onmessage:
                    self.onmessage(message)
            except:
                self.disconnect()
                break

    def disconnect(self):
        self.Socket.sendall(str(Message(msg_type="disconnect", content="bye", source=self.username)).encode())
        self.Socket.close()
        self.logger.info("[ - ] Disconnected from server.")