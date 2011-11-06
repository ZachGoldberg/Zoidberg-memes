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

from meem_models import Template, URICounter, get_all_templates, get_template_by_id,\
    get_all_template_ids, create_template, create_meme, get_meme_by_id, code_is_valid,\
    BetaTicket, get_all_memes


class LandingPortal(webapp.RequestHandler):

    def get(self):
        # disable caching for landing portal HTML (images still cached)
        # maintains freshness when user uploads new template
        self.response.headers['Cache-Control']="no-cache"

        template_uid = self.request.get('tuid') or '714783ff9d4c4248'
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
        meme_absurl = 'http://www.waterlol.com/serve?t=m&id=' + meme_id # temporary. make this dynamic before release
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
                self.response.headers['Content-Type'] = 'image/png'
                self.response.out.write(t.img)
        elif image_type == 'm': # meme requested
            m = get_meme_by_id(img_id)
            if scale !='t': #thumb
                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(m.meme)
            else:
                self.response.headers['Content-Type'] = 'images/jpeg'
                self.response.out.write(m.thumb)

# yeah....
class AddCode(webapp.RequestHandler):
    def get(self):
        c = BetaTicket(code="omguwbeta")
        c2 = BetaTicket(code="googleinterns2011")

        c.put()
        c2.put()

class InitURICounters(webapp.RequestHandler):
    def get(self):
        u1 = URICounter(key_name="1", count=1, counters_total=20)
        u1.put()
        u2 = URICounter(key_name="2", count=2, counters_total=20)
        u2.put()
        u3 = URICounter(key_name="3", count=3, counters_total=20)
        u3.put()
        u4 = URICounter(key_name="4", count=4, counters_total=20)
        u4.put()
        u5 = URICounter(key_name="5", count=5, counters_total=20)
        u5.put()
        u6 = URICounter(key_name="6", count=6, counters_total=20)
        u6.put()
        u7 = URICounter(key_name="7", count=7, counters_total=20)
        u7.put()
        u8 = URICounter(key_name="8", count=8, counters_total=20)
        u8.put()
        u9 = URICounter(key_name="9", count=9, counters_total=20)
        u9.put()
        u10 = URICounter(key_name="10", count=10, counters_total=20)
        u10.put()
        u11 = URICounter(key_name="11", count=11, counters_total=20)
        u11.put()
        u12 = URICounter(key_name="12", count=12, counters_total=20)
        u12.put()
        u13 = URICounter(key_name="13", count=13, counters_total=20)
        u13.put()
        u14 = URICounter(key_name="14", count=14, counters_total=20)
        u14.put()
        u15 = URICounter(key_name="15", count=15, counters_total=20)
        u15.put()
        u16 = URICounter(key_name="16", count=16, counters_total=20)
        u16.put()
        u17 = URICounter(key_name="17", count=17, counters_total=20)
        u17.put()
        u18 = URICounter(key_name="18", count=18, counters_total=20)
        u18.put()
        u19 = URICounter(key_name="19", count=19, counters_total=20)
        u19.put()

        # fuck yeah vim; i never need to learn how 2 loops.

### THIS SHIT SHOULD BE PART OF SOME KIND OF INITIALIZATION PKG



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
        # disable caching for meme gallery HTML (images still cached)
        self.response.headers['Cache-Control']="no-cache"

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
        #        (r'/initURICounters', InitURICounters), 
        #        (r'/addCode', AddCode), # yeah...........
        (r'/procTemplate', AddTemplate)],
    debug=False)
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
