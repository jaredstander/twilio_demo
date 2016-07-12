#!/usr/local/bin/python
from flask import Flask, flash, redirect, render_template, \
  request, url_for
from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio.rest.lookups import TwilioLookupsClient
# from werkzeug.wrappers import Request, Response
import os
import re
import yaml

with open("keys.yaml", 'r') as stream:
  try:
    keys = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)

app = Flask(__name__)

account_sid = keys["account_sid"]
auth_token  = keys["auth_token"]
client = TwilioRestClient(account_sid, auth_token)

@app.route('/sms', methods=['POST'])
# respond to inbound message

def respond():

  inbound = request.values.get('Body')
  inbound = re.sub(r"\s|\D|\W", "", inbound)

  if len(inbound) != 10:
    response = twiml.Response()
    message = response.message("Error: number doesn't have exactly 10 digits!", sender = keys["my_number"])

    return str(response)
  else:
    account_sid = keys["account_sid"]
    auth_token  = keys["auth_token"]
    lookup = TwilioLookupsClient(account_sid, auth_token)
    number = lookup.phone_numbers.get(inbound, include_carrier_info=True)

    response = twiml.Response()
    message = response.message("Number Owner: {0}.Carrier: {1}. Type: {2}. Error code (if any): {3}".format(str(number.carrier['name']), str(number.carrier['type']), str(number.carrier['error_code']))
, sender = keys["my_number"], action = keys["ngrok_url"] + "sms_callback")
    return str(response)


if __name__ == '__main__':
  app.run(debug=True)