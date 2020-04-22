class Phone:
    name = None
    num = None
    description = None

    def __init__(self,name):
        self.name = name

    def encodeJSON(self):
        pass

    def __str__(self):
        return  self.name