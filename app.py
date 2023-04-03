from os import environ
from urllib.parse import quote_plus
from cherrypy import quickstart, expose, request
from cherrypy import tools, config
from requests import post

OWED_AMOUNT = environ.get("OWED_AMOUNT", "17.00")

TO_EMAIL = environ.get("EMAIL_TO")
FROM_EMAIL = environ.get("EMAIL_FROM")
EMAIL_SUBJECT = environ.get("EMAIL_SUBJECT").encode("iso-8859-1")
MAILGUN_API = environ.get("MAILGUN_API_KEY")
MAILGUN_URL = environ.get("MAILGUN_URL")

COUNTER_PARTY_UID = environ.get("COUNTER_PARTY_UID", "4c72b098-74f5-43f2-a7e5-e6685f535c4d")

SETTLEUP_USERNAME = environ.get("SETTLEUP_USERNAME")
SETTLEUP_MESSAGE = environ.get("SETTLEUP_MESSAGE")

def sendMail():
  messageUrlEncode = quote_plus(SETTLEUP_MESSAGE)
  settleUpUrl = f"https://settleup.starlingbank.com/{SETTLEUP_USERNAME}/pay?amount={OWED_AMOUNT}&message={messageUrlEncode}"

  post(
    MAILGUN_URL,
    data={
      "from": FROM_EMAIL,
      "to": [TO_EMAIL.split(",")],
      "subject": EMAIL_SUBJECT,
      "html": f"Tap <a href='{settleUpUrl}'>here</a> to pay"
    },
    auth=("api",MAILGUN_API)
  )

class TransactionNotify(object):
  @expose
  @tools.json_in()
  def starling(self):
    counterPartyUid = request.json['content']['counterPartyUid']
    if counterPartyUid == COUNTER_PARTY_UID:
      sendMail()

config.update({
  "server.socket_host": "0.0.0.0"
})

quickstart(TransactionNotify())