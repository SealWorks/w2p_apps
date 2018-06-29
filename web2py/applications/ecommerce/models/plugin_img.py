# -*- coding: utf-8 -*-

db.define_table(
    'img',
    Field('alt'),
    Field('slug', requires=[IS_SLUG(), IS_NOT_IN_DB(db, 'img.slug')]),
    Field('img', 'upload'),
    Field('img_file', 'blob'),
    Field('transparency', 'boolean'),
    Field('tags', 'list:string')
)