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


def iugu_teste_py():
    from gluon.tools import fetch
    import urllib, base64
    url = "https://api.iugu.com/v1/invoices?"
    token = appconfig.get("iugu.token")
    base64string = base64.encodestring('%s:%s' % (token, "")).replace('\n', '')
    data = {}
    data['creat_at_from'] = "2018-07-01"
    data['limit'] = 10
    data['start'] = 0
    url += urllib.urlencode(data)
    r = json.loads(fetch(url, headers={'Authorization': "Basic %s" % base64string}))
    return {'url': url, 'r': r}
    #import mymodule
    # l = mymodule.year_month_dict(from_date='2017-12-01', to_date='2018-01-01')
    # return locals()

def test_cache():
    import time
    from gluon import current
    d = {'bool':False}
    t1 = time.ctime()
    d = current.cache.ram('t', lambda: func_aux(d), 3)
    t2 = time.ctime()
    return dict(time_call=t1,time_return=t2, r=d)


def cache_in_ram():
    import time
    t = cache.ram('time', lambda: time.ctime(), time_expire=5)
    d = dict(time=t, link=A('click me', _href=request.url), cache=cache.ram.stats)
    return response.render(d)


def func_aux(d):
    import time
    time.sleep(5)
    d['bool']=True
    #return datetime.today().strftime("%b %d, %Y")
    return datetime.today().strftime("%d-%m-%Y")

def form_pra_que_te_quero():
    db.define_table('esclerose',
                    Field('stinguinha', 'string'),
                    Field('textinho', 'text'),
                    Field('booleaninho', 'boolean'),
                    Field('interina', 'integer'),
                    Field('dobradinha', 'double'),
                    Field('bicentenarinha', 'decimal(2,4)'),
                    Field('datinha', 'date'),
                    Field('tempinho', 'time'),
                    Field('tipinho'),
                    )
    db.define_table('multipla',
                    Field('stinguinha', 'string'),
                    Field('textinho', 'text'),
                    Field('booleaninho', 'boolean'),
                    Field('interina', 'integer'),
                    Field('dobradinha', 'double'),
                    Field('bicentenarinha', 'decimal(2,4)'),
                    Field('datinha', 'date'),
                    Field('tempinho', 'time'),
                    Field('tipinho'),
                    )
    form = SQLFORM(db.esclerose)
    if form.process().accepted:
        response.flash = "you got it!"
    if form.errors:
        response.flash = "all you need is love"
    return dict(form=form)
