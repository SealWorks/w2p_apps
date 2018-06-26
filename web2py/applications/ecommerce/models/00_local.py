# -*- coding: utf-8 -*-

from gluon.admin import apath
from gluon.custom_import import track_changes
from gluon.fileutils import listdir
from gluon.myregex import regex_longcomments, regex_expose

track_changes(True)


def safe_read(a, b='r'):
    safe_file = open(a, b, encoding="utf8")
    try:
        return safe_file.read()
    finally:
        safe_file.close()

def find_exposed_functions(dt):
    dt = regex_longcomments.sub('', dt)
    return regex_expose.findall(dt)

def beauty_text(t):
    parts = t.split('_')
    return ' '.join([x.title() for x in parts])

import inspect
# when using the same globals() an exception is thrown
# for k, v in globals().copy().iteritems():
#     print(k, v)
#     if inspect.isfunction(v):
#         argspec = inspect.getargspec(v)
#
#         # anything else to check?
#         if len(argspec.args) == 0 and argspec.varargs is None and argspec.keywords is None:
#             # then this is a function of the current controller
#             pass

response.tmpmenu = UL(_class='collapsible')
controllers = sorted( listdir(apath('ecommerce/controllers/', r=request), '.*\.py$'))
controllers = [x.replace('\\', '/') for x in controllers]
for c in controllers:
    li = LI()
    _c = c[:-3]
    data = safe_read(apath('ecommerce/controllers/%s' % c, r=request))
    items = find_exposed_functions(data)
    li.append(DIV(beauty_text(_c), _class='collapsible-header'))
    body = UL()
    for i in sorted(items):
        body.append(LI(A(beauty_text(i), _href=URL(_c, i))))
    li.append(DIV( body, _class='collapsible-body'))
    response.tmpmenu.append(li)
