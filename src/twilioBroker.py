__author__ = 'georgevanburgh'
from twilio.rest import TwilioRestClient


class TwilioBroker:
    ACCOUNT_SID = "AC3700d9ec5419d1a4405e9e7338a7fd72"
    AUTH_TOKEN = "38788b60b0b530ad894ca81d77541a96"
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def playMp3ToUser(self, phoneNumber, trackUrl):
        call = self.client.calls.create(
                to=phoneNumber,
                from_="+441163262273",
                url=trackUrl,
                method="GET",
                fallback_method="GET",
                status_callback_method="GET",
                record="false"
)