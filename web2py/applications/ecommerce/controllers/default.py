# -*- coding: utf-8 -*-


def index():
    return dict(message="hello from default.py")



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    if(request.args(0)=='profile'): redirect(URL('default','profile'))
    return dict(form=auth())

@auth.requires_login()
def profile():
    #auth.user é o objeto que contem os dados do usuário logado guardados na tabela auth_user
    form = SQLFORM(db.clients, db.auth_user)
    return dict(form = form)


@auth.requires(lambda: auth.has_membership('app_admin'))
def _ah():
    tablename = request.args(0)
    if tablename: grid = SQLFORM.smartgrid(db[tablename])
    else: grid = UL(*[LI(A(t, _href=URL(args=t))) for t in db.tables])
    return dict(grid=grid)
