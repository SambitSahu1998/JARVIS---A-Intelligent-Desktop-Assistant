from twilio.rest import Client

account_sid='AC10a0b6b18279c555f2d0e8a7ee431e2b'
auth_token='b2c1ecd49dcf0999bfda573c9516654d'
Client=Client(account_sid,auth_token)

call=Client.calls.create(twiml='<Response>Hello This is Sambit Kumar Sahu</Response/>',
                        to='+918763216294',
                        from_='+19498281238')



print(call.sid)