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
import pprint

# Load my twilio keys and good secret stuff.
with open("keys.yaml", 'r') as stream:
  try:
    keys = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)

app = Flask(__name__)

account_sid = keys["account_sid"]
auth_token  = keys["auth_token"]
client = TwilioRestClient(account_sid, auth_token)

# Root page
@app.route('/', methods=['GET'])
def root():
  return "Text a 10-digit phone number to " + keys["my_number"] + " for number information."

# Post path for twilio data
@app.route('/sms', methods=['POST'])
def respond():

  inbound = request.values.get('Body')
  inbound = re.sub(r"\s|\D|\W", "", inbound)

  if len(inbound) != 10:
    message = client.messages.create(to = keys["my_number"], from_ = keys["my_twilio_number"], body = "Error: number doesn't have exactly 10 digits!")
  else:
    number = TwilioLookupsClient(account_sid, auth_token).phone_numbers.get(inbound, include_carrier_info = True)
    message = "Carrier name: " + str(number.carrier['name']) + ";  Carrier Type: " + str(number.carrier['type']) + ";  Error Code:" + str(number.carrier['error_code'])
    resp = twiml.Response()
    resp.message(message)
    return str(resp)

# @app.route('/sms_callback', methods=["POST"])
# def respond():
#   return "thing"

if __name__ == '__main__':
  app.run(debug=True)