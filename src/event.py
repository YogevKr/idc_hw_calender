class Event:
    def __init__(self, id, course, ex_number, end_time, link):
        self.id = id
        self.course = course
        self.ex_number = ex_number
        self.end_time = end_time
        self.link = link


    def set_end_time(self, new_end_time):
        self.end_time = new_end_time

    def __cmp__(self, other):
        return self.__dict__ == other.__dict__
