#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
import requests
import json
import math

class myDexchain:
    def __init__(self, host, port, mother, password):
        self.host = host
        self.port = port
        self.mother = mother
        self.password = password
        self.description = 'Description'
        print(".: Create Dexchain is DONE :.")
    
    def getBalance(self, wallet):
        try:
            url = "http://{}:{}/balanceWallet/{}".format(self.host, self.port, wallet)
            req = requests.post(url = url, data = '')
            data = req.json()
            if(data['result'] == '0000'):
                return data['value']
            else:
                return 0
        except requests.ConnectionError:
            print('Dexchain Api Bağlantı Hatası')
            self.dexLog('Dexchain Api Bağlantı Hatası')
            return 0
        except ConnectionError as e:
            self.dexLog('{}'.format(e))
            return 0

    def getTokenBalance(self, wallet, contract):
        try:
            url = "http://{}:{}/balanceToken/{}&{}".format(self.host,self.port,wallet,contract)
            req = requests.post(url = url, data = '')
            data = req.json()
            if(data['result'] == '0000'):
                return data['value']
            else:
                return 0
        except requests.ConnectionError:
            print('Dexchain Api Bağlantı Hatası')
            self.dexLog('Dexchain Api Bağlantı Hatası')
            pass
        except ConnectionError as e:
            self.dexLog('{}'.format(e))
            return 0

    def send(self, sender, password, receiver, amount, contract, description):
        try:
            url = "http://{}:{}/sendTransaction/{}&{}&{}&{}&IN&{}&Webitox".format(self.host, self.port, sender, password, receiver, amount, contract, description)
            req = requests.post(url = url, data = '')
            data = req.json()
            print(data)
            self.dexLog('{}'.format(data))
            if(data['result'] == '0000'):
                return 1
            elif(data['result'] == '0010'):
                print(data)
                self.dexLog('{}'.format(data))
                return 0
            else:
                print(data)
                self.dexLog('{}'.format(data))
                return 0
        except requests.ConnectionError:
            print('Dexchain Api Bağlantı Hatası')
            self.dexLog('Dexchain Api Bağlantı Hatası')
            return 0
        except ConnectionError as e:
            self.dexLog('{}'.format(e))
            return 0

    def sendMother(self, sender, contract, password, amount):
        if(contract == None):
            contract = 'mydexchain'
        return self.send(sender, password, self.mother, amount, contract,self.description)

    def sendForInsufficient(self, wallet, amount):
        send = math.ceil(self.fee(amount))
        return self.send(self.mother,self.mpass,wallet,send,'mydexchain',self.description)

    def dexLog(self, strMessage):
        t = datetime.now()
        fileName = 'log/{}-{}-{}_log.txt'.format(t.year,t.month,t.day)
        LogFile = open(fileName,'a')
        LogFile.write(strMessage+'\n')
        LogFile.close()

    def fee(order):
        if order > 0 and order <= 1000:
            fee = order * 0.003
        elif order > 1000 and order < 10000:
            order = order - 1000
            fee = (order * 0.0003) + 3
        elif order > 10000 and order < 100000:
            order = order - 10000
            fee = (order * 0.00003) + 5.70
        elif order > 100000 and order < 1000000:
            order = order - 100000
            fee = (order * 0.000003) + 8.40
        elif order > 1000000 and order < 10000000:
            order = order - 1000000
            fee = (order * 0.0000003) + 11.10
        elif order > 10000000 and order < 100000000:
            order = order - 10000000
            fee = (order * 0.00000003) + 13.80
        elif order > 100000000 and order < 1000000000:
            order = order - 100000000
            fee = (order * 0.000000003) + 16.50
        elif order > 1000000000 and order < 10000000000:
            order = order - 1000000000
            fee = (order * 0.0000000003) + 19.20
        elif order > 10000000000 and order < 100000000000:
            order = order - 10000000000
            fee = (order * 0.00000000003) + 21.09
        elif order > 100000000000 and order < 1000000000000:
            order = order - 100000000000
            fee = (order * 0.000000000003) + 24.60
        return fee

    def setDescription(self, strDesc):
        self.description = strDesc
