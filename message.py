class Message:
    # Message format <type>:::<content>
    separator = ":::"

    def __init__(self, string = None, msg_type = None, content = None, *args, **kwargs):
        self.string = string
        self.type = msg_type
        self.content = content

    @classmethod
    def from_string(string):
        msg = Message(string)
        msg.type, msg.content = msg.string.split(Message.separator)
        return msg

    @classmethod
    def from_content(msg_type, content):
        msg = Message(msg_type, content)
        msg.string = f"{msg.type}{Message.separator}{msg.content}"
        return msg.string

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string