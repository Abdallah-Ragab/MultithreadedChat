class Message:
    # Message format <type>:::<content>
    separator = ":::"

    def __init__(self, data = None, msg_type = None, content = None, *args, **kwargs):
        self.data = data
        self.type = msg_type
        self.content = content

    @classmethod
    def decode(data):
        msg = Message(data)
        msg.type, msg.content = msg.data.split(Message.separator)
        return msg

    @classmethod
    def encode(msg_type, content):
        msg = Message(msg_type, content)
        msg.data = f"{msg.type}{Message.separator}{msg.content}"
        return msg.data

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data