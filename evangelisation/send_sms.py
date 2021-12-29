from twilio.rest import Client
from django.conf import settings

def send_sms(message):
    account_id = 'AC4406ad8c9ba51725edde77315b2674cb'
    auth_token = '04c64a103f11ec2ebed4d2128f76a121'
    
    for receiver in message.receiver_message.all():
        try:
            client = Client(account_id, auth_token)
            message = client.messages.create(
                body=f"{message.body}",
                from_="+15005550006",
                to=f"+237{receiver.telephone}"
            )
            print("==================envoie reussie============")
            return True
        except:
            print("==================EEEEEEERRRRRRRRROOOOOOOOOOOORRRRRRRRR============")
            return False