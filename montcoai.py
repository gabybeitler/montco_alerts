#!/usr/bin/env python3

import re
import urllib.request
from twilio.rest import Client
from itertools import product
from bs4 import BeautifulSoup as bs

account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

file = open('/home/montcocad/lib/last_alert.txt', 'r+')

url = "https://webapp02.montcopa.org/eoc/cadinfo/livecadrss.asp"

with urllib.request.urlopen(url) as response:
    xml = response.read()

x = file.read().splitlines()
soup = bs(xml, 'lxml')

newalert = []
known_alert = []

description = soup.find_all(['description'])
title = soup.find_all(['title'])

count = 0

# Grab the township we want to alerts

for eachd in description:
    #print(eachd)
    if 'WHITEMARSH' in eachd.string:
        t1 = re.sub('<.*?>', '', str(title[count])).strip()
        d1 = eachd.string.strip()
        newalert.append(t1 + ": " + d1)
    elif 'CONSHOHOCKEN' in eachd.string:
        t1 = re.sub('<.*?>', '', str(title[count])).strip()
        d1 = eachd.string.strip()
        newalert.append(t1 + ": " + d1)
    elif 'PLYMOUTH' in eachd.string:
        t1 = re.sub('<.*?>', '', str(title[count])).strip()
        d1 = eachd.string.strip()
        newalert.append(t1 + ": " + d1)
    count = count + 1



for eacha in x:
    if 'WHITEMARSH' in eacha:
        known_alert.append(eacha)
    elif 'CONSHOHOCKEN' in eacha:
        known_alert.append(eacha)
    elif 'PLYMOUTH' in eacha:
        known_alert.append(eacha)

for x, y in product(newalert, known_alert):
    if x == y:
        newalert.remove(x)

newalert_count = len(newalert)

if newalert_count > 0:
    for c in newalert:
        newalert_count -= 1
        file.write(newalert[newalert_count] + '\n')
        client.messages.create(
        to = '',
        from_ = '',
        body = newalert[newalert_count]
        )
