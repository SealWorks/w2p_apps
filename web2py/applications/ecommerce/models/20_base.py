db.define_table('loja_products',
                           Field('product', 'string', label='Product'),
                           Field('description', 'text', label='Description'),
                           Field('codes', 'json', label='Codes')
                           )

db.define_table('loja_suppliers',
                            Field('name', 'string', label='Name'),
                            Field('cnpj', 'integer', label='CNPJ'),  # TODO add validador
                            # contato
                            Field('address', 'string', label='Address'),
                            Field('zip', 'string', label='ZIP'),  # TODO add validador
                            Field('phone', 'string', label='Telephone'),  # TODO add validador
                            Field('email', 'string', label='E-mail', requires=IS_EMAIL(error_message='invalid email!'))
                            )

db.define_table('clients',
                Field('user_id','integer'),#integer para poder ser vazio
                Field('email'),
                Field('name'),
                Field('cpf_cnpj', label='CPF/CNPJ'),
                Field('iss', 'integer', label='ISS'),
                Field('phone_prefix', 'string', label=T('Phone Prefix')),
                Field('phone', 'string', label=T('Telephone')),
                Field('user_refs','json')
                )

db.define_table('address',
                Field('client_id','reference clients'),
                Field('name'),
                Field('is_main','boolean'),#,requires=IS_IN_SET(['Cobrança','Entrega'])),
            #---dados do enderesso
                Field('zip', 'string', label=T('ZIP')),
                Field('street', 'string', label=T('Street')),
                Field('home_number', 'string', label=T('Number')),
                Field('district', 'string', label=T('District')),
                Field('city', 'string', label=T('City')),
                Field('country_state', 'string', label=T('State')),
                Field('country', 'string', label=T('Country')),
                Field('complement', 'string', label=T('Comnplement'))
                )
# BODY PARAMS
# Email do cliente	OBRIGATÓRIO
# Nome do cliente	OBRIGATÓRIO
# Notas
# Número do Telefone - 9 dígitos
# Prefixo, apenas números - 3 dígitos (obrigatório caso preencha "phone")
# CPF ou CNPJ do cliente. Obrigatório para emissão de boletos registrados.
# Endereços de E-mail para cópia separados por vírgula
# CEP. Obrigatório para emissão de boletos registrados
# Número do endereço (obrigatório caso "zip_code" seja enviado).
# Rua. Obrigatório caso CEP seja incompleto.
# Cidade
# Estado
# Bairro. Obrigatório caso CEP seja incompleto.
# Complemento de endereço. Ponto de referência.
# Variáveis Personalizadas {name:**;value:**}

db.define_table('sells',
                        Field('product', 'reference loja_products', label='Product'),
                        Field('client', 'reference clients'),
                        Field('forma_de_pagamento')
                        )

db.define_table('buys',
                       Field('product', 'reference loja_products', label='Product'),
                       Field('suppliers', 'reference loja_suppliers'),
                       Field('forma_de_pagamento')
                       )
