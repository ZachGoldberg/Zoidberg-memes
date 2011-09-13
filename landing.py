#!/usr/bin/env python

# waterlol landing page
# Amir Sayed Khader, Qifan Xi
# askhader@uwaterloo.ca, qxi@uwaterloo.ca


from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache


class LandingPortal(webapp.RequestHandler):

    def get(self):

        self.response.out.write("Dicks")


class ServeImage(webapp.RequestHandler):
    def get(self):
        img_name = self.request.get('n')
        #self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(
        


def main():
    application = webapp.WSGIApplication([
        (r'/', LandingPortal),
        (r'/m', ServeImage],
    debug=False)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
