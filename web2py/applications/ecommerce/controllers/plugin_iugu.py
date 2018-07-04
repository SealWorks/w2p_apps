# -*- coding: utf-8 -*-


def index():
    # main_address = db(db.address.user_id == auth.user_id and db.address.is_main==True).select()
    return dict()


def get_users():
    return iugu.get_users()


def new_invoice():
    bill_form = SQLFORM(db.plugin_iugu_bills)
    # TODO optional fields
    # TODO: CNPJ adicionar um campo de ISS

    if bill_form.process().accepted:
        # session.resp = iugu.new_invoice(bill_form.vars)
        redirect(URL('visualizar_fatura', args=[bill_form.vars.id]))

    elif bill_form.errors:
        session.flash = "Errou no cliente!"

    # TODO form validators
    return dict(form=bill_form)


def list_invoices():
    form = SQLFORM.factory(
        Field('customer_id'),
        Field('created_at_from', 'date'),
        Field('created_at_to', 'date'),
        Field('paid_at_from', 'date'),
        Field('paid_at_to', 'date'),
        Field('due_date', 'date'),
        Field('updated_since', 'date'),
        Field('filtros',
              requires=IS_IN_SET(iugu.invoice_status, multiple=True))
    )
    page = request.args(0) or 0
    filters = {}
    iugu_bills = {}
    if form.process(keepvalues=True).accepted:
        for key, value in form.vars.iteritems():
            if value:
                if key in ['customer_id', 'filtros']:
                    filters[key] = value
                else:
                    from datetime import datetime
                    filters[key] = datetime.strftime(datetime.strptime(value, "%b %d, %Y"), iugu.date_format)

        iugu_bills = iugu.get_invoices(page=page, filters=filters)
    return dict(bills=iugu_bills, form=form)


def segunda_via():
    if request.args:
        bill = iugu.get_duplicate(request.args(0))
    else:
        bill = {}
    return dict(bill=bill)


def new_customer():
    return dict()


# @auth.requires_login()
def list_custumers():
    list = iugu.list_customers()
    return dict(clients=list)
