import requests
from requests.auth import HTTPBasicAuth

class Iugu:
    url = "https://api.iugu.com/v1/"


    def __init__(self, token):
        self.token = token
        self.auth  = HTTPBasicAuth(token, '')

    def get_users(self):
        url = self.url + 'customers'
        response = requests.get(url, auth= self.auth)
        return response.text

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