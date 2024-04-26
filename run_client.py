import random
import threading
import time
from client import Client


names = [
    "Abdallah",
    "Mohamed",
    "Ahmed",
    "Ali",
    "Omar",
    "Khaled",
    "Youssef",
    "Hassan",
    "Hussein",
    "Sayed",
    "Khalil",
    "Khalid",
    "Mona",
    "Nada",
    "Nour",
    "Noura",
    "Noha",
    "Nada",
    "Nadia",
    "Naglaa",
    "Nahla",
    "Nahed",
    "Nahla",
    "Naila",
    "Najla",
    "Najat",
    "Najwa",
    "Nariman",
    "Nashwa",
]


client = Client(username=random.choice(names))


def msg():
    time.sleep(5)
    client.send("Hello, World!")


threading.Thread(target=msg).start()

client.connect()
