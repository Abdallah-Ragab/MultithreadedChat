import threading
import time
from client import Client

client = Client()
def msg():
    time.sleep(5)
    client.send("Hello, World!")

threading.Thread(target=msg).start()

client.connect()
