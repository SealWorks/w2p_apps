# -*- coding: utf-8 -*-

def index():
    user = auth.user
    groups = auth.user_groups
    return locals()


@auth.requires_login()
def setup():
    if not db.auth_group(role='app_admin'):
        auth.add_membership(auth.add_group('app_admin'))
    session.flash = "Setup done!"
    return redirect(URL('teste_local', 'index'))

@auth.requires_membership('app_admin')
def populate_me():
    from gluon.contrib.populate import populate
    if request.args(0):
        form = SQLFORM.factory(Field('quantity', 'integer'))
        if form.process().accepted:
            qtd = abs(int(form.vars.quantity or 1))
            populate(db[request.args(0)], qtd)
            response.flash = 'Populated with ' + str(qtd) + ' data!'

        elif form.errors:
            response.flash = 'oh nooos'
        rows = db(db[request.args(0)]).select()
    else:
        grid = UL(*[LI(A(t, _href=URL(args=t))) for t in db.tables])
    return locals()



def iugu_teste_py2():
    from gluon.tools import fetch
    import urllib2, base64
    url = "https://api.iugu.com/v1/invoices/"
    token = appconfig.get("iugu.token")
    base64string = base64.encodestring('%s:%s' % (token, "")).replace('\n', '')
    r = fetch(url, headers={'Authorization': "Basic %s" % base64string})
    return r