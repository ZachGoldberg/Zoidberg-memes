#!/usr/bin/env python

import uuid

def generate_uuid( digits ):

    while True:
        tmp = min(digits, 32)
        uid = uuid.uuid4().hex[:tmp]
        digits -= 32
        if digits <= 32:
            break

    return uid
