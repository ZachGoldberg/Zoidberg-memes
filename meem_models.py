#!/usr/bin/env python

# waterlol data models

import logging

from google.appengine.ext import db, webapp
from google.appengine.api import users

class Template(db.Model):
    """Model for storing meem templates"""
    uid = db.StringProperty()
    name = db.StringProperty()
    img = db.BlobProperty(default=None)
    thumb = db.BlobProperty(default=None)

def get_all_templates():
    """Return all availabel templates"""
    ts = {}
    targets = ['uid', 'name', 'thumb']
    for t in Template.all():
        ts[t.uid] = t.name
    return ts

def get_all_template_ids():
    """Return a list of template uids"""
    return [t.uid for t in Template.all()]

def get_template_by_id(uid):
    return Template.all().filter('uid =', uid).get()
