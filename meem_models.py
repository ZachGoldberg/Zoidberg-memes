#!/usr/bin/env python

# waterlol data models

import logging, random

from google.appengine.ext import db, webapp
from google.appengine.api import users
from google.appengine.api.images import Image, resize, JPEG

from util import generate_uuid

class Meme(db.Model):
    """Finalized meem"""
    uid = db.StringProperty()
    top = db.StringProperty()
    bottom = db.StringProperty()
    meme = db.BlobProperty(default=None)
    thumb = db.BlobProperty(default=None)
    meme_width = db.IntegerProperty
    meme_height = db.IntegerProperty
    template_uid = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True)


# create_meme(str, str, str) [ the third string is the raw meme in base64 encoding]
def create_meme(top, bottom, meme, template_uid):
    """Create a meme object in the datastore"""
    m = Image(meme)
    thumb = Image(meme)
    width, height = m.width, m.height

    if m.width != 500:
        m.resize(width=500)
        m = m.execute_transforms(output_encoding=JPEG)

        moar_img_data = Image(m)
        width, height = moar_img_data.width, moar_img_data.height

        meme = db.Blob(m)
    else:
        logging.info("There")
        meme = db.Blob(meme)

    thumb.resize(height=125)
    thumb = thumb.execute_transforms(quality=85,output_encoding=JPEG)
    thumb = db.Blob(thumb)

    meme = Meme(uid=str(get_meme_url()),
                top=top,
                bottom=bottom,
                meme=meme,
                meme_width=width,
                meme_height=height,
                thumb=thumb,
                template_uid=template_uid)
    meme.put()
    return meme


def get_meme_by_id(uid):
    return Meme.all().filter('uid =', uid).get()

def get_all_memes():
    ms = []
    for m in Meme.all():
        ms.append((m.uid, m.timestamp))
    sorted(ms, key=lambda meme: meme[1],reverse=False)
    ms.reverse()
    return ms

class Template(db.Model):
    """Model for storing meem templates"""
    uid = db.StringProperty()
    name = db.StringProperty()
    img = db.BlobProperty(default=None)
    thumb = db.BlobProperty(default=None)
    real_width = db.IntegerProperty()
    real_height = db.IntegerProperty()


# create_template(str, str) [ the second string is the raw image ]
def create_template(name, img):
    """Adds this template to the datastore along with a generated
       thumbnail and accompanied dimension metadata"""
    
    thumb = Image(img)
    template_data = Image(img)
    t_img = db.Blob(img)
    width, height = template_data.width, template_data.height

    if width != 548:
        template_data.resize(width=548)
        template_data = template_data.execute_transforms()
        t_data = Image(template_data)
        width, height = t_data.width, t_data.height
        t_img = db.Blob(template_data)

    thumb.resize(height=125)
    thumb = thumb.execute_transforms(quality=75,output_encoding=JPEG)

    t = Template(uid=generate_uuid(16),
                 name=name,
                 img=t_img,
                 thumb=db.Blob(thumb),
                 real_width=width,
                 real_height=height)
    t.put()

def get_all_templates():
    """Return all available templates uids with dimension information"""
    ts = []
    for t in Template.all():
        ts.append((t.uid, t.name, t.real_width, t.real_height))
    return ts

def get_all_template_ids():
    """Return a list of template uids"""
    return [t.uid for t in Template.all()]

def get_template_by_id(uid):
    return Template.all().filter('uid =', uid).get()


class BetaTicket(db.Model):
    """Model for storing meem templates"""
    code = db.StringProperty()


def code_is_valid(code):
    return True
 

class URICounter(db.Model):
    count = db.IntegerProperty(indexed=True, required=True)
    counters_total = db.IntegerProperty(indexed=False,default=20)
    
    def get_next(self):
        c = self.count
        self.count += self.counters_total
        self.put()
        return c

def get_unique_code():
    """Get a counter at random and return an unused code"""
    counter_index = random.randint(0,19)
    counter = URICounter.get_by_key_name(str(counter_index))
    if not counter:
        counter = URICounter(count=counter_index)
        counter.save()
    c = counter.get_next()
    return c

ALPHABET = 'ZbDYFQLXx0PsHtmIcC2GA1qjB78VUdywJThkpnfWrOgSKu3olM59RizE64vNae'
def enc_b62(num):
    """Encode a number to base 62"""
    if num == 0:
        return ALPHABET[0]
    ret = []
    while num:
        rem = num % 62
        num = num // 62
        ret.append(ALPHABET[rem])
    ret.reverse()
    return ''.join(ret)

def get_meme_url():
    c = enc_b62(get_unique_code())
    return c
