#!/usr/bin/python

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import logging

# models
from meem_models import URICounter, Meme, enc_b62

class InitCodes( webapp.RequestHandler ):
    """Run this script to initialize the counters for the willt
       url code generators"""

    def get(self):
        n = 0
        for i in range(20):
            ac = URICounter(count=i,
                             total_counter_nums=20,
                             key_name = str(i))
            ac.put()
            n += 1


class FixCodes(webapp.RequestHandler):

    def get(self):
        m = Meme.all()
        for mm in m:
            logging.info(mm.uid)
            mm.uid = enc_b62(int(mm.uid))
            mm.put()
        self.response.out.write("All failiures went undetected")
        


def main():
    application = webapp.WSGIApplication([(r'/init', InitCodes),
                                          (r'/initFix', FixCodes)], debug=False)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

