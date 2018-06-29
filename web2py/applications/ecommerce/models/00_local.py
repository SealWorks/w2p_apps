# -*- coding: utf-8 -*-

from gluon.custom_import import track_changes
track_changes(True)


from gluon.admin import apath
from gluon.fileutils import listdir
from gluon.myregex import regex_longcomments, regex_expose


def safe_read(a, b='r'):
    try:
        safe_file = open(a, b, encoding="utf8")
    except TypeError:
        safe_file = open(a, b)
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
