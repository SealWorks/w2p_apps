# -*- coding: utf-8 -*-
def index():
    return dict(message="hello from ecommerce².py")


@auth.requires_login()
def profile():
    #auth.user é o objeto que contem os dados do usuário logado guardados na tabela auth_user

    codigo = ""
    #c = db(db.clients.user_id == auth.user_id).select()
    #c[0] == client
    client = db.clients(db.clients.user_id == auth.user_id)
    form = SQLFORM(db.clients,record=client,showid=False)
    form.vars.user_id = auth.user_id
    client_address = db(db.address.user_id == auth.user_id).select()

    if form.process(keepvalues=True).accepted:
        response.flash = 'Thanks for filling the form'
        if iugu:
            # payload = {"email":"jana","name":"aa","notes":"aa","phone":1,"phone_prefix":1,"cpf_cnpj":"a","cc_emails":"a",
            #            "zip_code":"a","number":1,"street":"a","city":"a","state":"a","district":"a","complement":"a",
            #            "default_payment_method_id":"a","custom_variables":[{"name":"a","value":"a","_destroy":"true"}]}
            #payload =
            iugu.new_cliente(form.vars)
    return dict(form=form,table = client_address)


@auth.requires_login()
def add_address():
    form = SQLFORM(db.address,showid=False)
    form.vars.user_id = auth.user.id
    form.vars.is_main = (db.address(db.address.user_id == auth.user_id) is None)
    if form.process().accepted:
        response.flash = 'Thanks for filling the form'
        redirect('profile')
    return dict(form=form, user=form.vars.is_main)


@auth.requires(lambda: auth.has_membership('app_admin'))
def _ah():
    tablename = request.args(0)
    if tablename: grid = SQLFORM.smartgrid(db[tablename])
    else: grid = UL(*[LI(A(t, _href=URL(args=t))) for t in db.tables])
    return dict(grid=grid)
