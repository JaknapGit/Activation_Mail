from django.shortcuts import render
from .serializer import User, UserSerial
from rest_framework.views import APIView
from rest_framework.response import Response
from .tokens import account_activation_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import EmailThread
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings


class UserView(APIView):
    def get(self, request):
        post = User.objects.all()
        serializer = UserSerial(post, many=True)
        return Response(data=serializer.data, status = 200)

    '''
    def post(self, request):
        serializer = UserSerial(data = request.data)
        subject = 'User Creation Activation mail'
        message = 'Dear user to activate user account click the link below :- f{}'
        user_email = request.data.get('email')
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=200)
        return Response({'details':'Data may not be valid.'})
    '''

    def post(self, request):
        try:
            serializer = UserSerial(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            obj.is_active=False
            obj.save()
            domain = get_current_site(request=request).domain
            token = account_activation_token.make_token(obj)
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            relative_url = reverse('activate', kwargs={'uidb64':uid, 'token':token})
            absolute_url = 'http://%s'%(domain+relative_url,)
            message = 'Hello %s. \n\tThank you for creating account. Click below to activate your account\n %s'%(obj.username, absolute_url)
            subject = 'Account Activation Email'
            EmailThread(subject=subject, message=message, recipient_list=[obj.email], from_email=settings.EMAIL_HOST_USER).start()
            return Response(data={'detail':'Please check your email for account activation'}, status=201)
        
        except Exception as e:
            print(e)
            return Response(data=serializer.errors, status=400)
        

class UserAccountActivate(APIView):

    def get(self, request, uidb64, token):
        try:
            uid= force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            return Response(data={'detail':'There is an error'}, status=400)
        if account_activation_token.check_token(user=user, token=token):
            user.is_active=True
            user.save()
            return Response(data={'detail': 'Account Activated Successfully...'}, status=200)
        return Response(data={'detail':'Activation link invalid'}, status=400)
