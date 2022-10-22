class RequestBoard:
    def __init__(self, date, time, start_loc, dest, description, capacity, owner=None):
        self.date = date
        self.time = time
        self.start_loc = start_loc
        self.dest = dest
        self.description = description
        self.capacity = capacity
        self.owner = owner

    @staticmethod
    def checkValidation(board):
        return True