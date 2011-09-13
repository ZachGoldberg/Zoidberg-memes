#!/usr/bin/env python

# waterlol landing page
# Amir Sayed Khader, Qifan Xi
# askhader@uwaterloo.ca, qxi@uwaterloo.ca

import os

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
        #self.response.out.write(


class ShowAddTemplate(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/landing.html')
        self.response.out.write(template.render(path, template_values))
        
    
    def post(self):



def main():
    application = webapp.WSGIApplication([
        (r'/', LandingPortal),
        (r'/m', ServeImage),
        (r'/addTemplate', ShowAddTemplate),
        (r'/procTemplate', ProcAddTemplate)],
    debug=False)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
