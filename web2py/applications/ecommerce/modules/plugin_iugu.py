# -*- coding: utf-8 -*-
from gluon.tools import fetch
import json, base64, urllib
from datetime import datetime
from gluon import current


class Iugu:
    url = "https://api.iugu.com/v1/"

    def __init__(self, token):
        self.token = token
        base64string = base64.encodestring('%s:%s' % (token, "")).replace('\n', '')
        self.headers = {'Authorization': "Basic %s" % base64string}

    def get_users(self):
        url = self.url + 'customers'
        response = requests.get(url, auth=self.auth)
        return response.json()

    def new_invoice(self, bill):
        url = self.url + 'invoices'

        address = {}
        payer = {}
        payload = {}
        for key, value in bill:
            if key.startswith('address_'):
                address[key[8:]] = value
        payload = dict(email=bill['your_email'], due_date=bill['due_date'],
                       items=bill['items'], payer=payer)

        return requests.request("POST", url, json=payload, auth=self.auth)

    def get_invoices(self, page=0, filters=dict()):
        status = {'pending', 'paid', 'canceled', 'partially_paid', 'refund', 'expired', 'authorized'}
        url = self.url + 'invoices'
        data={'limit':10}
        url += '?'+urllib.urlencode(data)
        print(url)
        r = fetch(url, headers=self.headers)
        return r


    def get_duplicate(self, id):
        invoice = self.get_invoices(id)
        due_date = datetime.strptime(invoice['due_date'], "%Y-%m-%d")
        today = datetime.today()
        if today <= due_date:
            return invoice
        else:
            url = self.url + 'invoices/' + id + '/duplicate'
            payload = dict(
                due_date=due_date.strftime("%Y-%m-%d")  # OBRIGATÓRIO  AAAA - MM - DD.
                # items = [], #Adicione, altere ou remova  itens
                #             #Para remover, envie "id" do subitem + "_destroy=true"
                #             # description ="",
                #             # quantity =
                #             # price_cents
                #             # id
                #             # _destroy
                # ignore_due_email =False, #Ignora o envio do e - mail de cobrança da nova fatura.
                # ignore_canceled_email = False, #Ignora o envio do e - mail de cancelamento da nova fatura.
                # current_fines_option = True, #aplica (true) as multas da fatura original
                # keep_early_payment_discount= False
            )
            response = requests.post(url, auth=self.auth, json=payload)
            return response.json()

    # {
    # --------client data
    #     "id": "3F9866DD932C41A198EBF2442B7B2708",
    #     "email": "jana@rmail.com",
    #     "name": "Jana",
    #     "cpf_cnpj": null,
    #     "cc_emails": null,
    #     "notes": null,
    #     "custom_variables": [],
    #     "default_payment_method_id": null,
    #     "proxy_payments_from_customer_id": null,
    #     "created_at": "2018-06-25T16:50:33-03:00",
    #     "updated_at": "2018-06-25T16:50:33-03:00",
    # -----contact data
    #     "zip_code": null,
    #     "number": null,
    #     "complement": null,
    #     "phone": null,
    #     "phone_prefix": null,
    #     "city": null,
    #     "state": null,
    #     "district": null,
    #     "street": null
    # }
    def list_customers(self):
        url = self.url + "customers"
        response = requests.get(url, auth=self.auth)
        r_json = response.json()
        return r_json['items']

    def new_customers(self, vars):
        url = self.url + "customers"
        payload = vars
        response = requests.request("POST", url, data=payload)
        resp_json = response.json()
        return resp_json  # ["id"]

    def update_customer(self, id_iugu):
        url = self.url + "customers/" + id_iugu
        # payload = {"email":"jana","name":"aa","notes":"aa","phone":1,"phone_prefix":1,"cpf_cnpj":"a","cc_emails":"a",
        #            "zip_code":"a","number":1,"street":"a","city":"a","state":"a","district":"a","complement":"a",
        #            "default_payment_method_id":"a","custom_variables":[{"name":"a","value":"a","_destroy":"true"}]}
        response = requests.request("PUT", url)
        return response.json()
