#!/usr/bin/python

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

# models
from meem_models import URICounter

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

def main():
    application = webapp.WSGIApplication([(r'/init', InitCodes)], debug=False)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

