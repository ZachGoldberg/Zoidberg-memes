#!/usr/bin/env python

# waterlol data models

import logging

from google.appengine.ext import db, webapp
from google.appengine.api import users
from google.appengine.api.images import Image, resize

from util import generate_uuid

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
    t_img = db.Blob(img)
    template_data = Image(img)
    width, height = template_data.width, template_data.height

    thumb.resize(height=125)
    thumb = thumb.execute_transforms(quality=70)

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
