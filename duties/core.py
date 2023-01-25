
# # import os
# # from pyexpat.errors import messages
# # from twilio.rest import Client
# # # Find your Account SID and Auth Token at twilio.com/console
# # # and set the environment variables. See http://twil.io/secure
# # def sms(phone , message):
# #     account_sid ='AC1088fcfd72e630a6096bf8aa6b2803d0'
# #     auth_token = '90e4291b4ce5e60ac3ab25aef68d3b50'
# #     client = Client(account_sid, auth_token)
# #     print(message)
# #     message = client.messages.create(
# #                                         body=message,
# #                                         from_='+13608456360',
# #                                         to=phone
# #                                     )

# #     print(message.sid)
# # --------------------------------------------------------------------------------------------------


# # import urllib.request
# # import urllib.parse
 
# # def sendSMS(apikey, numbers, sender, message):
# #     data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
# #         'message' : message, 'sender': sender})
# #     data = data.encode('utf-8')
# #     request = urllib.request.Request("https://api.textlocal.in/send/?")
# #     f = urllib.request.urlopen(request, data)
# #     fr = f.read()
# #     return(fr)
 
# # resp =  sendSMS('NGE1NTVhN2E3MzUyNmQ3MDZlNTQ0MjMwNjkzMTU2NTQ=', '918123456789',
# #     'Jims Autos', 'This is your message')
# # print (resp)










# # /--------------------------------------------------------------------------------------------

# import logging
# from celery import shared_task

# from time import sleep

# from textlocal_python import TextLocalClient


# logging.basicConfig(level="INFO")
# logger = logging.getLogger("BIDDANO")

# @shared_task
# def send_sms(phone_numbers, message):
#     client = TextLocalClient(apikey="NGE1NTVhN2E3MzUyNmQ3MDZlNTQ0MjMwNjkzMTU2NTQ=")
#     for tries in range(3):
#         response = client.send_message(
#             phone_numbers, message, sender="vijay"
#         )
#         if response[0]["status"]=="success":
#             break
#         else:
#             sleep(0.1)
#     logger.info(response)    
  