from rest_framework import generics,permissions
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from .utils import Util
import jwt
from django.conf import settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.http import Http404
import random




class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        username = user.get('username','')
        email = user.get('email','')
        if User.objects.filter(username=username,email=email).exists():
            return Response({'status':'error','message':'Username and Email already exists'})
        if User.objects.filter(username=username).exists():
            return Response({'status':'error','message':'Username already exists'})
        if User.objects.filter(email=email).exists():
            return Response({'status':'error','message':'Email already exists'})
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # token = RefreshToken.for_user(user).access_token
        
        
        # email_body = 'Hi '+user.username + '\n Your One Time Password will be \n' + str(otp)
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Register In Eshop!! | One Time Password'}
        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


def cheange_password(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        user = User.objects.get(id=payload['user_id'])
        return render(request,'user/password.html',{'user':user})

    except jwt.ExpiredSignatureError as identifier:
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as identifier:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordChange(generics.GenericAPIView):
    def post(self,request):
        user = request.data
        username = user['username']
        new_pass = user['new_pass']
        confirm_pass = user['confirm_pass']
        if new_pass != confirm_pass:
            return Response({'error': 'password not matched'}, status=status.HTTP_200_OK)
        user = User.objects.get(username=username)
        print(user)
        user.set_password(confirm_pass)
        user.save()
        return Response({'success': 'password change succesfully'}, status=status.HTTP_201_CREATED)


class ResetPassword(generics.GenericAPIView):
    def post(self,request):
        user = request.data
        username = user['username']
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404

        email = user.email
        token = RefreshToken.for_user(user).access_token
        
        current_site = get_current_site(request).domain
        relativeLink = reverse('change-pass')
        absurl = "http://localhost:3000/pass-change?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to set your new password \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Reset your password'}
        # print(data)
        Util.send_email(data)
        return Response({'msg':'password rest mail is sent to your given mail address'}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        email = request.data.get('email')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'email': 'User already verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

