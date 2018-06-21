Products = db.define_table('loja_products',
                           Field('product', 'string', label='Product'),
                           Field('description', 'text', label='Description'),
                           Field('codes', 'json', label='Codes')
                           )

Suppliers = db.define_table('loja_suppliers',
                            Field('name', 'string', label='Name'),
                            Field('cnpj', 'integer', label='CNPJ'),  # TODO add validador
                            # contato
                            Field('address', 'string', label='Address'),
                            Field('zip', 'string', label='ZIP'),  # TODO add validador
                            Field('phone', 'string', label='Telephone'),  # TODO add validador
                            Field('email', 'string', label='E-mail', requires=IS_EMAIL(error_message='invalid email!'))
                            )

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

Sells = db.define_table('sells',
                        Field('product', 'reference loja_products', label='Product'),
                        Field('client', 'reference plugin_iugu_clients'),
                        Field('forma_de_pagamento')
                        )

Buys = db.define_table('buys',
                       Field('product', 'reference loja_products', label='Product'),
                       Field('suppliers', 'reference loja_suppliers'),
                       Field('forma_de_pagamento')
                       )
