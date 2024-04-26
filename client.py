import logging
import socket
from message import Message


class Client:

    default_server_host = "127.0.0.1"
    default_server_port = 99
    username = "Anonymous"

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
        self.logger.info("[ i ] Listening for messages.")

        self.send(self.username, msg_type="handshake")

        self.listen_for_messages()

    def send(self, message, msg_type="message"):
        msg = Message(msg_type=msg_type, content=message, source=self.username)
        encoded_msg = str(msg).encode()
        self.logger.info(f"[ + ] Sent message: {message}")
        self.Socket.sendall(encoded_msg)

    def listen_for_messages(self):
        while True:
            raw_message = self.Socket.recv(1024).decode()
            message = Message(string=raw_message)
            if message.type in ["announcement", "message"]:
                self.logger.info(f"[ ⇩ ] {message.display}")