from datetime import datetime

from google.appengine.ext import ndb


class AppModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)


class LogEntry(AppModel):
    student_id = ndb.StringProperty(required=True)  # TODO: Move terminology away from students
    time_out = ndb.DateTimeProperty()
    time_in = ndb.DateTimeProperty()

    def flip(self):
        if self.time_in:
            if self.time_out:
                new_record = LogEntry(student_id=self.student_id, time_out=self.time_in)
                new_record.put()
            else:
                self.time_out = self.time_in
                new_record = self
            self.time_in = None
            self.put()
            return new_record
        else:  # TODO: What if the second-to-last entry had no time_in?  Then should we shove it back onto that one?
            # ...though that would never happen when coming from a scan because it would have checked that up front.
            self.time_in = self.time_out
            self.time_out = None
            self.put()
            return self

    @classmethod
    def scan_student_id(cls, student_id):  # TODO: Should this just be a function in the handler, not a class method?
        record = cls.query(cls.student_id == student_id).order(-cls.updated).get()
        now = datetime.now()
        if not record or record.time_in:
            record = cls(student_id=student_id, time_out=now)
        else:  # TODO: Check time since last and maybe max out at an hour?
            record.time_in = now
            # TODO: Calculate time_gone?
        record.put()
        return record
