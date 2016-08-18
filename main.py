import urllib

import webapp2

import models
import template


class AppHandler(webapp2.RequestHandler):
    pass


class EntryHandler(AppHandler):
    def get(self, entry_id):
        record = models.LogEntry.get_by_id(int(entry_id))
        self.response.write(template.render('entry', {
            'record': record
        }))


class MainHandler(AppHandler):
    def get(self):
        records = models.LogEntry.query().order(-models.LogEntry.created)  # TODO: Limit
        self.response.write(template.render('index', {
            'barcode': self.request.get('barcode'),
            'entries': records,
            'scan_return_url': urllib.quote('http://192.168.1.47:8080/scan/{CODE}'),  # TODO: Fix URL
        }))


class ScanHandler(AppHandler):
    def process_scan(self, *args):
        try:
            barcode = args[0]
        except IndexError:
            barcode = self.request.get('barcode')
        record = models.LogEntry.scan_student_id(student_id=barcode)
        self.redirect('/entry/' + str(record.key.id()))  # TODO: urlsafe?

    def get(self, *args):
        self.process_scan(*args)

    def post(self, *args):
        self.process_scan(*args)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/entry/(.*)', EntryHandler),
    ('/scan', ScanHandler),
    ('/scan/(.*)', ScanHandler)
], debug=True)
