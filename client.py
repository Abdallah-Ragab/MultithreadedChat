import logging
import socket
from message import Message


class Client:

    default_server_host = "127.0.0.1"
    default_server_port = 99

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, ip=None, port=None):
        ip = ip or self.default_server_host
        port = port or self.default_server_port

        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.connect((ip, port))
        self.logger.info(f"[ + ] Connected to server {ip}:{port}")

    def send(self, message):
        msg = Message.from_content("message", message)
        encoded_msg = str(msg).encode()
        self.Socket.sendall(encoded_msg)

    def listen_for_messages(self):
        while True:
            message = self.Socket.recv(1024).decode()
            self.logger.info(f"Received message: {message}")