# -*- coding: utf-8 -*-
import base64
import json
import urllib
from datetime import datetime, timedelta
from gluon import current
from gluon.tools import fetch


def year_month_dict(from_date=None, to_date=None, format='%Y-%m-%d'):
    if from_date is None:
        from_date = datetime.today()
        month = from_date.month
        year = from_date.year
        start = year * 100 + month
    else:
        from_date = datetime.strptime(from_date, format)
        start = int(from_date.strftime('%Y%m'))
        month = start % 100
        year = start / 100

    if to_date is None:
        to_date = datetime.today()
        end = to_date.year * 100 + to_date.month
    else:
        to_date = datetime.strptime(to_date, format)
        end = int(to_date.strftime('%Y%m'))

    if start > end:
        return ValueError.message("from_date cannot be bigger them to_date")

    d = dict()
    while start <= end:
        d[str(start)] = {'first_day': datetime(year, month, 01).date()}
        month += 1
        if month == 13:
            year += 1
            month = 1
        d[str(start)]['last_day'] = (datetime(year, month, 01).date() + timedelta(days=-1))
        start = year * 100 + month
    return d


class Iugu:
    url = "https://api.iugu.com/v1/"
    invoice_status = {'pending', 'paid', 'canceled', 'partially_paid', 'refund', 'expired', 'authorized'}
    date_format = "%Y-%m-%d"

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

        for key, value in bill:
            if key.startswith('address_'):
                address[key[8:]] = value
        payload = dict(email=bill['your_email'], due_date=bill['due_date'],
                       items=bill['items'], payer=payer)

        return requests.request("POST", url, json=payload, auth=self.auth)

    def get_invoices(self, page=0, filters=dict()):
        # type: (int, dict) -> list

        url = self.url + 'invoices?'
        payload = {'limit': (page + 1) * 1000, 'start': page * 1000}

        if 'customer_id' in filters:
            payload['customer_id'] = filters['customer_id']
            url += urllib.urlencode(payload)
            return [current.cache.ram(
                "invoices_ID_" + str(payload['customer_id']),
                lambda: json.loads(fetch(url, headers=self.headers)),
                144000  # 4h = 144000seg
            )]

        if 'created_at_from' in filters:
            if 'created_at_to' in filters:
                d = year_month_dict(from_date=filters['created_at_from'], to_date=filters['created_at_to'])
            else:
                d = year_month_dict(from_date=filters['created_at_from'])
        elif 'created_at_to' in filters:
            d = year_month_dict(to_date=filters['created_at_to'])
        else:
            url += urllib.urlencode(filters)
            return [json.loads(fetch(url, headers=self.headers))]

        invoices_monthly = []
        for key in d:
            payload['created_at_from'] = d[key]['first_day']
            payload['created_at_to'] = d[key]['last_day']
            url = self.url + 'invoices?' + urllib.urlencode(payload)
            invoices_monthly.append(current.cache.ram(
                "invoices_CA_" + key,
                lambda: json.loads(fetch(url, headers=self.headers)),
                144000  # 4h = 144000seg
            ))
        return invoices_monthly

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

# _________
