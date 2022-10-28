from http.client import ResponseNotReady
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from authentication import serializers

from authentication.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    ProfileSerializer, 
    ProfileUpdateSerializer,
    )

from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import jwt
from wowstore import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # user = User.objects.get(email=serializer.data['email'])
            # token = RefreshToken.for_user(user).access_token
            # current_site = get_current_site(request).domain
            # relativeLink = reverse('email_verify')
            # absurl='http://'+ current_site + relativeLink + "?token=" + str(token)
            # email_body = "Hi "+ user.username + ". This is wowstore.\nUse linke below to verify your email.\n\n" + absurl
            # data = {'email_body': email_body, 'to_email' : user.email,
            #         'email_subject' : '[Wowstore] Verify your email'}
            # Util.send_email(data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms= 'HS256')
            user = User.objects.get(pk=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email' : 'success'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error' : 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as identifier:
            return Response({'error' : 'Invalid toekn'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data
            access_token = str(token.access_token)
            refresh_token = str(token)
            return Response({
                                "refresh": refresh_token,
                                "access": access_token,
                            }, status=status.HTTP_200_OK
                            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class RequestPasswordResetEmailView(generics.GenericAPIView):
#     serializer_class = RequestPasswordResetEmailSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             pass


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    "message": "Password was wrong.",
                    "result": {},
                    "status": False,
                    "status_code": 400
                }, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.validated_data['password'])
            user.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     tokens = OutstandingToken.objects.filter(user_id=request.user.pk)
    #     for token in tokens:
    #         BlacklistedToken.objects.get_or_create(token=token)
    #     return Response(status=status.HTTP_200_OK)
            
class ProfileView(views.APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = get_object_or_404(User, pk=self.request.user.pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, pk=self.request.user.pk)
        serializer = ProfileUpdateSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
