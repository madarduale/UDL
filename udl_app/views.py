from django.shortcuts import render, redirect
from .models import Message
# Create your views here.
import jwt
from .jaas_jwt import JaaSJwtBuilder
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib import messages
from django.views import View
from .forms import (
    MessageForm
)

def home(request):
    return render(request, 'udl_app/home.html')
# def generate_jwt(user):
#     # Assuming your settings.py has defined these features:
#     # settings.JITS_FEATURES = {'livestreaming': 'false', 'outbound-call': 'false', ...}
#     # Note: you should adjust the features based on user permissions
#     features = settings.JITS_FEATURES

#     payload = {
#         'aud': 'jitsi',
#         'iss': 'chat',
#         'iat': datetime.now(timezone.utc),
#         'exp': datetime.now(timezone.utc) + timedelta(hours=1),
#         'nbf': datetime.now(timezone.utc) - timedelta(days=1),
#         'sub': 'vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7',
#         'context': {
#             'features': features,
#             'user': {
#                 'hidden-from-recorder': False,
#                 'moderator': user.is_staff,
#                 'name': user.username,
#                 'id': str(user.id),
#                 'avatar': user.profile.avatar.url if user.profile.avatar else '',
#                 'email': user.email
#             }
#         },
#         'room': '*'
#     }
    
#     private_key = settings.JWT_PRIVATE_KEY  # Your private key
#     # Make sure to define the algorithm and kid header
#     return jwt.encode(payload, private_key, algorithm='RS256', headers={
#         'alg': 'RS256',
#         'kid': 'vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7/2f5089',
#         'typ': 'JWT'
#     })



def generate_jwt(user):
    jaas_jwt = JaaSJwtBuilder()
    private_key = settings.JWT_PRIVATE_KEY.strip() 

    token = jaas_jwt.withDefaults() \
        .withApiKey("vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7/45e73f") \
        .withUserName(user.username) \
        .withUserEmail(user.email) \
        .withModerator(user.is_staff) \
        .withAppID("vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7") \
        .withUserAvatar(user.profile.avatar.url if user.profile.avatar else '') \
        .signWith(private_key)

    return token



def jitsi_meet(request):
    # jwt_token = generate_jwt(request.user)
    jwt_token = generate_jwt(request.user)
    # decoded_token = jwt.decode(jwt_token, verify=False, algorithms=['RS256']) 
    decoded_token = jwt_token.decode("utf-8")

    print(decoded_token)
    # jwt_token2='eyJraWQiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTQzYzA4ODIxMjVkNGUzOGJlYmE3N2Q1YjM2MDkzYTcvZWIwOWViLVNBTVBMRV9BUFAiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJqaXRzaSIsImlzcyI6ImNoYXQiLCJpYXQiOjE3MTQ4NTQyNTEsImV4cCI6MTcxNDg2MTQ1MSwibmJmIjoxNzE0ODU0MjQ2LCJzdWIiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTQzYzA4ODIxMjVkNGUzOGJlYmE3N2Q1YjM2MDkzYTciLCJjb250ZXh0Ijp7ImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOnRydWUsIm91dGJvdW5kLWNhbGwiOnRydWUsInNpcC1vdXRib3VuZC1jYWxsIjpmYWxzZSwidHJhbnNjcmlwdGlvbiI6dHJ1ZSwicmVjb3JkaW5nIjp0cnVlfSwidXNlciI6eyJoaWRkZW4tZnJvbS1yZWNvcmRlciI6ZmFsc2UsIm1vZGVyYXRvciI6dHJ1ZSwibmFtZSI6Im1hZGFyZHVjYWFsZTk5ODgiLCJpZCI6ImF1dGgwfDY2MzVkNTc4NjFhOTRkZGMzNjA2NzU5NCIsImF2YXRhciI6IiIsImVtYWlsIjoibWFkYXJkdWNhYWxlOTk4OEBnbWFpbC5jb20ifX0sInJvb20iOiIqIn0.TzxGx5krRc0AM7xKo0F5iHb6vZoGngmjj8uO-F-wHE_VTg9qVL_HS0nPuANP35jaiyZqJakWv3P2KZwCyCc49tCTk8XOc7MuHj7vWetKTdao-Kj_IC9gZipX2peBCeGWOdZe2gWQ-Skj2GT6-h90sl_D6916rdYonoKZBTwzjOOympJNh3YKAQ4DIbmiV4K34vgg2bY6wFRCBnVL5g5fQAbcVwIOIVco7gvJjCgukXwkho-wCRHl8VWJgDQKVVhBA-pGvsHU7v41kKLGRxyz6QK9FOfWML0mQikL7G9tOkj3tm0KXlUQESfUnDQbCpToZbsF9kzbMZBRPlELWP4-Ug'
    return render(request, 'udl_app/jitsi_meet.html', {'jwt_token': decoded_token})



def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox') 
    else:
        form = MessageForm()
    return render(request, 'udl_app/send_message.html', {'form': form})

def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    jwt_token = generate_jwt(request.user)
    decoded_token = jwt_token.decode("utf-8")
    print(decoded_token)
    message_urls = []  
    for message in received_messages:
        if message.url:
            meeting_url = f'{message.url}?jwt={decoded_token}'
            message_urls.append((message, meeting_url))
    return render(request, 'udl_app/inbox.html', {'message_urls':message_urls})