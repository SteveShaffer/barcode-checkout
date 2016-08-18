from datetime import datetime

from google.appengine.ext import ndb


class AppModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)


class LogEntry(AppModel):
    student_id = ndb.StringProperty(required=True)
    time_out = ndb.DateTimeProperty()
    time_in = ndb.DateTimeProperty()

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
