class Event:
    def __init__(self, id, course, ex_number, end_time, link, google_id=""):
        self.id = id
        self.course = course
        self.ex_number = ex_number
        self.end_time = end_time
        self.link = link
        self.google_id = google_id

    def set_end_time(self, new_end_time):
        self.end_time = new_end_time

    def __cmp__(self, other):
        return (self.id == other.id) and (self.end_time == other.end_time)
