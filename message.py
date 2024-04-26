class Message:
    # Message format <type>:::<content>
    separator = ":::"

    def __init__(self, string=None, msg_type=None, content=None, source=None, *args, **kwargs):
        self.string = string
        self.type = msg_type
        self.content = content
        self.source = source

        if string:
            self.type, self.source, self.content = string.split(Message.separator)
        elif msg_type and content and source:
            self.string = f"{msg_type}{Message.separator}{source}{Message.separator}{content}"
        else:
            raise ValueError("Invalid arguments. Either pass a string or msg_type, source, and content.")

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __dict__(self):
        return {
            "type": self.type,
            "source": self.source,
            "content": self.content
        }

    @property
    def display(self):
        return(f"{self.source}: {self.content}")
