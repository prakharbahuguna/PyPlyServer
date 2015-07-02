__author__ = 'georgevanburgh'
from twilio.rest import TwilioRestClient


class TwilioBroker:
    ACCOUNT_SID = "" # REDACTED
    AUTH_TOKEN = ""  # REDACTED
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def playMp3ToUser(self, phoneNumber, trackUrl):
        call = self.client.calls.create(
                to=phoneNumber,
                from_="", # REDACTED
                url=trackUrl,
                method="GET",
                fallback_method="GET",
                status_callback_method="GET",
                record="false"
)
