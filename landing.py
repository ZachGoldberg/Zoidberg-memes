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

from meem_models import Template, get_all_templates, get_template_by_id,\
    get_all_template_ids, create_template

class LandingPortal(webapp.RequestHandler):

    def get(self):
        templates = get_all_templates()
        logging.info(templates)
        template_data = {
            'templates': templates
        }
        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_data))


class ServeImage(webapp.RequestHandler):

    def get(self):
        image_type = self.request.get('t')
        img_id = self.request.get('id')
        scale = self.request.get('s')

        if image_type == 't': # template requested
            t = get_template_by_id(img_id)

            if scale == 't': #thumbnail requested
            #self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(t.thumb)
            else:
                self.response.out.write(t.img)
        #self.response.out.write(


class AddTemplate(webapp.RequestHandler):

    def get(self):
        status = self.request.get('s')
        template_values = {}
        template_values['status'] = '<h1 style="color: green;">Success</h1>' if status == 's' else ''
        path = os.path.join(os.path.dirname(__file__), 'html/addTemplate.html')
        self.response.out.write(template.render(path, template_values))
        
    
    def post(self):
        t_img = self.request.get('template')
        t_name = self.request.get('name')
        create_template(t_name, t_img)
        self.redirect('/addTemplate?s=s')

def main():
    application = webapp.WSGIApplication([
        (r'/', LandingPortal),
        (r'/serve', ServeImage),
        (r'/addTemplate', AddTemplate),
        (r'/procTemplate', AddTemplate)],
    debug=False)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
