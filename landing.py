#!/usr/bin/env python

# waterlol landing page
# Amir Sayed Khader, Qifan Xi
# askhader@uwaterloo.ca, qxi@uwaterloo.ca

import os, logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache

from meem_models import Template
from util import generate_uuid

class LandingPortal(webapp.RequestHandler):

    def get(self):
        dirs = os.listdir(".")
        self.response.out.write(str(dirs))


class ServeImage(webapp.RequestHandler):

    def get(self):
        img_name = self.request.get('n')
        #self.response.headers['Content-Type'] = 'image/jpeg'
        #self.response.out.write(


class AddTemplate(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/addTemplate.html')
        self.response.out.write(template.render(path, template_values))
        
    
    def post(self):
        t_img = self.request.get('template')
        t_name = self.request.get('name')
        t_img = db.Blob(t_img)
        logging.info(t_img)
        t = Template(uid=generate_uuid(16),
                     name=t_name,
                     img=t_img,
                     official=True)
        t.put()


def main():
    application = webapp.WSGIApplication([
        (r'/', LandingPortal),
        (r'/m', ServeImage),
        (r'/addTemplate', AddTemplate),
        (r'/procTemplate', AddTemplate)],
    debug=False)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
