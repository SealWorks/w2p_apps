def get_users():
    return iugu.get_users()


def gerar_fatura():

    bill_form = SQLFORM(db.plugin_iugu_bills)
    #TODO optional fields
    #TODO: CNPJ adicionar um campo de ISS

    if bill_form.process().accepted:
        #session.resp = iugu.gerar_fatura(bill_form.vars)
        redirect(URL('visualizar_fatura',args=[bill_form.vars.id]))

    elif bill_form.errors:
        session.flash = "Errou no cliente!"

    #TODO form validators
    return dict(form = bill_form)


def visualizar_faturas():
    if len(request.args) > 0:
        bills =[]
        for x in request.args:
            bills.append(iugu.get_bills(x))
    else:
        iugu_bills = iugu.get_invoices()
        bills = iugu_bills['items']

    return dict(bills = bills)

def segunda_via():
    bill = iugu.get_duplicate(request.args(0))
    return dict(bill = bill)