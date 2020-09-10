class Snack():
    def __init__(self, name):
        self.name = name
        self.description = ''
        self.price = 0.00
        self.image = 'default.png'
    
    def get_data(self):
        return self.__dict__