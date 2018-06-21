def get_users():
    return iugu.get_users()


def gerar_fatura():

    bill_form = SQLFORM(db.plugin_iugu_bills)
    #TODO optional fields
    #TODO: CNPJ adicionar um campo de ISS

    if bill_form.process().accepted:
        #session.resp = iugu.gerar_fatura(bill_form.vars)
        redirect('visualizar_fatura/' + str(bill_form.vars.id))

    elif bill_form.errors:
        session.flash = "Errou no cliente!"

    #TODO form validators
    return dict(form = bill_form)


def visualizar_fatura():
    r = request.vars
    return dict(r=r)


def visualizar_fatura2():
    payer_address = dict(zip_code="29200130", street="R sealworks", number="76", district="Centro", city="Guarapari",
                         state="ES", country="Brazil", complement="apt")
    payer = dict(cpf_cnpj="11879553708", name="Jana", phone_prefix="27", phone="9988336552", email="jana@email.com",
                 address=payer_address)

    form_payer = SQLFORM.dictform(payer)
    if form_payer.process().accepted:
        payer.update(form_payer.vars)
    elif form_payer.errors:
        session.flash = "Errou no cliente!"

    form_address = SQLFORM.dictform(payer_address)
    if form_address.process().accepted:
        payer.update(form_address.vars)
    elif form_address.errors:
        session.flash = "Errou no endereço!"

    session.counter = (session.counter or 0) + 1
    session.list = (session.list or [])
    item = dict(quantity='1', price_cents='100', description="descricao")
    form_item = SQLFORM.dictform(item)
    session.list.append('1')
    if form_item.process().accepted:
        print('bbbbbbb')
        print(form_item)
        session.list.append(form_item)
    elif form_item.errors:
        print('ccccc')
        session.flash = "Errou no item!"
    else:
        print('Primeiro form a aparecer')

    due_date = '2018-06-17'
    email = 'janascal@email.com'
    return dict(form_payer=form_payer, form_item=form_item, form_address=form_address, intems=session.list,
                counter=session.counter)
    # return dict(r=iugu.gerar_fatura(payer=payer, items=list,due_date=due_date, email=email))
