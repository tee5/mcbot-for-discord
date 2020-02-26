#!/usr/bin/env python
# coding: utf-8

import json
import requests

class Conoha(object):
    def __init__(self):
        pass
    def get_token(self):
        url = "https://identity.tyo1.conoha.io/v2.0/tokens"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "auth": {
                "passwordCredentials": {
                    "username": "xxxxxxxxxxxxx",
                    "password": "xxxxxxxxxxxxx"
                },
                "tenantId": "xxxxxxxxxxxxxxxxxxxxxx"
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    def restart(self):
        url = "https://compute.tyo1.conoha.io/v2/xxxxxxxxxxxxxxxxxxxxxxx/servers/xxxxxxxxxxxxxxxxxxxxx/action"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": self.get_token()["access"]["token"]["id"]
        }
        payload = {
            "reboot": {
                "type": "SOFT"
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response
        
