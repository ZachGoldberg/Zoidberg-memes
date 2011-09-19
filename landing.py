#!/usr/bin/env python

# waterlol landing page
# Amir Sayed Khader, Qifan Xi
# askhader@uwaterloo.ca, qxi@uwaterloo.ca

import os, logging, base64, re

import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import memcache

from meem_models import Template, get_all_templates, get_template_by_id,\
    get_all_template_ids, create_template, create_meme, get_meme_by_id, code_is_valid,\
    BetaTicket, get_all_memes


class LandingPortal(webapp.RequestHandler):

    def get(self):
        template_uid = self.request.get('tuid')
        templates = get_all_templates()
        template_data = {
            'templates': templates,
            'template_uid': template_uid
        }
        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_data))

    dataURLPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    def post(self):
        """Meme Upload Handler"""
        theMeme = self.request.get('meme')
        top = self.request.get('top')
        bottom = self.request.get('bottom')
        template_uid = self.request.get('tuid')
        theMeme64 = self.dataURLPattern.match(theMeme).group(2)
        m = create_meme(top,bottom,base64.b64decode(theMeme64),template_uid)
        self.redirect('/m' + m.uid)


class ShowMeme(webapp.RequestHandler):
    def get(self, meme_id):
        m = get_meme_by_id(meme_id)

        logging.info(m)
        if m is None:
            self.redirect('/')
            return

        meme_relurl = 'serve?t=m&id='+meme_id;
        meme_absurl = 'http://dev.waterlol.com/serve?t=m&id=' + meme_id # temporary. make this dynamic before release
        page_url = self.request.url;

        meme_data = {
            'meme_relurl': meme_relurl,
            'meme_author' : 'N/A',
            'meme_absurl': cgi.escape(meme_absurl),
            'page_url' : cgi.escape(page_url),
            'page_href' : cgi.escape('<a href="' + page_url + '">meme!</a>'),
            'meme_img' : cgi.escape('<img src="' + meme_absurl + '" / >'),
            'template_uid': m.template_uid
        }
        
        path = os.path.join(os.path.dirname(__file__), 'html/meme.html')
        self.response.out.write(template.render(path, meme_data))


class ServeImage(webapp.RequestHandler):

    def get(self):
        self.response.headers.add_header("Expires", "Thu, 01 Dec 2014 16")
        self.response.headers['Cache-Control']="public, max-age=3660000"

        image_type = self.request.get('t')
        img_id = self.request.get('id')
        scale = self.request.get('s')

        if image_type == 't': # template requested
            t = get_template_by_id(img_id)

            if scale == 't': #thumbnail requested
                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(t.thumb)
            else:
                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(t.img)
        elif image_type == 'm': # meme requested
            m = get_meme_by_id(img_id)
            if scale !='t': #thumb
                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(m.meme)
            else:
                self.response.out.write(m.thumb)


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
        code = self.request.get('code')
        if code_is_valid(code):
            create_template(t_name, t_img)
            self.redirect('/addTemplate?s=s')
        else:
            self.redirect('/addTemplate')

class MemeGallery(webapp.RequestHandler):

    def get(self):
        memes = get_all_memes()
        logging.info(memes)
        template_values = { 'memes': memes }
        path = os.path.join(os.path.dirname(__file__), 'html/meme_gallery.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([
        (r'/', LandingPortal),
        (r'/m(.*)', ShowMeme),
        (r'/r', MemeGallery),
        (r'/addMeme', LandingPortal),
        (r'/serve', ServeImage),
        (r'/addTemplate', AddTemplate),
        (r'/procTemplate', AddTemplate)],
    debug=False)
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
