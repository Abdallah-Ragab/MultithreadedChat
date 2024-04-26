class Message:
    # Message format <type>{:}<content>
    def __init__(self, data, *args, **kwargs):
        self.data = data
        self.type = None
        self.content = None
        self.decode()
    def decode(self):
        self.type, self.content = self.data.split("{:}")