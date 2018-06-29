# -*- coding: utf-8 -*-


@auth.requires(lambda: auth.has_membership('app_admin'))
def index():
    response.view = 'generic.html'
    grid = SQLFORM.smartgrid(db.img)
    return dict(grid=grid)
