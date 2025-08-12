from django.shortcuts import render
from .models import CustomUser
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'status':status.HTTP_201_CREATED})
        return Response({'message':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'data':serializer.validated_data, 'status':status.HTTP_200_OK})
        return Response({'data':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class LogoutAPI(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': "Avtorizatsiya qilinmagan foydalanuvchi"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            request.user.auth_token.delete()
            return Response({'msg': "Siz dasturdan chiqdingiz"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPI(APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response({'data':serializer.data,
             'status':status.HTTP_200_OK})

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data,
                             'status': status.HTTP_200_OK})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})





