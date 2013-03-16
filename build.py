#!/usr/bin/env python

import glob
import time
import re
import io
import base64

def readfile(fn, flags='U', encoding='utf8'):
    with io.open(fn, flags + 'r', encoding=encoding) as f:
        return f.read()

def loaderString(var):
    fn = var.group(1)
    return readfile(fn).replace('\n', '\\n').replace('\'', '\\\'')

def loaderRaw(var):
    fn = var.group(1)
    return readfile(fn)

def loaderBase64(var):
    fn = var.group(1)
    return base64.b64encode(str(readfile(fn, flags='b', encoding=None)))

c = '\n\n'.join(map(readfile, glob.glob('code/*')))
n = time.strftime('%Y-%m-%d-%H%M%S')
m = readfile('main.js')

m = m.split('@@INJECTHERE@@')
m.insert(1, c)
m = '\n\n'.join(m)

m = m.replace('@@BUILDDATE@@', n)
m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
m = re.sub('@@INCLUDEBASE64:([0-9a-zA-Z_./-]+)@@', loaderBase64, m)

with io.open('iitc-debug.user.js', 'w', encoding='utf8') as f:
    f.write(m)

# vim: ai si ts=4 sw=4 sts=4 et
