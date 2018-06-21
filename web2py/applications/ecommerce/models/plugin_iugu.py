from plugin_iugu import Iugu

iugu = Iugu(appconfig.get("iugu.token"))

if not Clients:
    Clients = db.define_table('plugin_iugu_clients',
                              Field('name', label='Nome/Razão Social'),
                              Field('cpf_cnpj', label='CPF/CNPJ'),
                              Field('iss', 'integer', label='ISS'),
                              # ---------------------contato
                              Field('email', 'string', label='E-mail'),
                              Field('phone_prefix', 'string', label=T('Phone Prefix')),
                              Field('phone', 'string', label=T('Telephone')),
                              Field('zip', 'string', label=T('ZIP')),
                              Field('street', 'string', label=T('Street')),
                              Field('home_number', 'string', label=T('Number')),
                              Field('district', 'string', label=T('District')),
                              Field('city', 'string', label=T('City')),
                              Field('country_state', 'string', label=T('State')),
                              Field('country', 'string', label=T('Country')),
                              Field('complement', 'string', label=T('Comnplement'))
                              )


Bills = db.define_table('plugin_iugu_bills',
                        Field('due_date', 'date', label=T("Due Date")),
                        Field('email', label=T("E-mail")),
                        Field('items_list', 'list:integer', label=T("Items")),
                        Field('client', 'reference clients', label=T("Client")),
                        Field('id_iugu', readble=False, writable=False)
                        )


Bill_items = db.define_table('plugin_iugu_bill_items',
                             Field('quantity', 'integer', label=T("Quantity"), requires=IS_INT_IN_RANGE(1, 10000000)),
                             Field('price_in_cents', 'integer', label=T("Price"), requires=IS_NOT_EMPTY()),
                             Field('description', 'text', label=T('Description'), requires=IS_NOT_EMPTY()),
                             Field('bill', 'reference plugin_iugu_bills')
                             )