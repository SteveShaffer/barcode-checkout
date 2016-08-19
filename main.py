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
            'record': record,
            'allow_flip': self.request.get('fresh') == 'yes'
        }))


class EntryFlipHandler(AppHandler):
    def post(self, entry_id):
        record = models.LogEntry.get_by_id(int(entry_id))
        record = record.flip()
        self.redirect('/entry/{}/?fresh=yes'.format(record.key.id()))


class MainHandler(AppHandler):
    def get(self):
        records = models.LogEntry.query().order(-models.LogEntry.updated).fetch(20)
        self.response.write(template.render('index', {
            'barcode': self.request.get('barcode'),
            'entries': records,
            'scan_return_url': urllib.quote(self.request.host_url + '/scan?barcode={CODE}'),
            'show_manual': self.request.get('manual') == 'yes'
        }))


class ScanHandler(AppHandler):
    def process_scan(self):
        barcode = self.request.get('barcode')
        record = models.LogEntry.scan_student_id(student_id=barcode)
        self.redirect('/entry/{}/?fresh=yes'.format(record.key.id()))  # TODO: urlsafe?

    def get(self):
        self.process_scan()

    def post(self):
        self.process_scan()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/entry/(.*)/flip', EntryFlipHandler),
    ('/entry/(.*)/', EntryHandler),
    ('/scan', ScanHandler),
], debug=True)
