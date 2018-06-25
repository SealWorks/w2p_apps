import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

class Iugu:
    url = "https://api.iugu.com/v1/"


    def __init__(self, token):
        self.token = token
        self.auth  = HTTPBasicAuth(token, '')

    def get_users(self):
        url = self.url + 'customers'
        response = requests.get(url, auth= self.auth)
        return response.json()

    def gerar_fatura(self,bill):
        url = self.url+'invoices'

        address={}
        payer={}
        payload = {}
        for key,value in bill:
            if key.startswith('address_'):
                address[key.subs]
        payload = dict(email=bill['your_email'], due_date=bill['due_date'],
                       items=bill['items'], payer=payer)

        return requests.request("POST", url, json=payload, auth=self.auth)


    def get_invoices(self, id=None):
        url = self.url + 'invoices/'
        if id: url += id
        response = requests.get(url, auth=self.auth)
        return response.json()

    def get_duplicate(self,id):
        invoice = self.get_invoices(id)
        due_date = datetime.strptime(invoice['due_date'], "%Y-%m-%d")
        today = datetime.today()
        if today <= due_date:
            return invoice
        else:
            url = self.url + 'invoices/'+id +'/duplicate'
            payload = dict(
                due_date = due_date.strftime("%Y-%m-%d")#OBRIGATÓRIO  AAAA - MM - DD.
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