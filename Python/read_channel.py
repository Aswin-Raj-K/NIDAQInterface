class Reader:
    def __init__(self, num, name, time_shown=0.25):
        self.num = num
        self.name = name
        self.time_shown =time_shown
            
    def get_id(self):
        return int(self.num)
    
    def get_name(self):
        return self.name

    def get_time_shown(self):
        return self.time_shown
        