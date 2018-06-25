from plugin_iugu import Iugu

iugu = Iugu(appconfig.get("iugu.token"))

db.define_table('plugin_iugu_bills',
                        Field('due_date', 'date', label=T("Due Date")),
                        Field('email', label=T("E-mail")),
                        Field('items_list', 'list:integer', label=T("Items")),
                        Field('client', 'reference clients', label=T("Client")),
                        Field('id_iugu')
                        )


db.define_table('plugin_iugu_bill_items',
                             Field('quantity', 'integer', label=T("Quantity"), requires=IS_INT_IN_RANGE(1, 10000000)),
                             Field('price_in_cents', 'integer', label=T("Price"), requires=IS_NOT_EMPTY()),
                             Field('description', 'text', label=T('Description'), requires=IS_NOT_EMPTY()),
                             Field('bill', 'reference plugin_iugu_bills')
                             )