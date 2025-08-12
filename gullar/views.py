from django.shortcuts import render
from .models import Gullar
from .serializer import GullarSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from account.user_perm import IsUser


class ListCreateAPI(GenericAPIView):
    queryset = Gullar.objects.all()
    serializer_class = GullarSerializer

    def get(self, request):
        gullar = self.get_queryset()
        serializer = self.get_serializer(gullar, many=True)
        data = {
            'data':serializer.data,
            'count':len(gullar),
            'status':status.HTTP_200_OK
        }

        return Response(data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'messages':'muvaffaqiyatli yaratildi'})
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'error':serializer.errors})

class DetailUpdateDeleteApi(GenericAPIView):
    queryset = Gullar.objects.all()
    serializer_class = GullarSerializer

    def get_object(self, pk):
        gul = Gullar.objects.get(id=pk)
        return gul

    def get(self, request, pk):
        gul = self.get_object(pk=pk)
        serializer = GullarSerializer(gul)
        data = {
            'data':serializer.data,
            'status':status.HTTP_200_OK
        }

        return Response(data)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    permission_classes = [permissions.IsAuthenticated, IsUser, ]
    def put(self, request, pk):
        try:
            gul = self.get_object(pk=pk)
        except Gullar.DoesNotExist:
            return Response({
                'status':status.HTTP_404_NOT_FOUND, 'message':'Bunday soat topilmadi'
            })
        serializer = GullarSerializer(gul, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'data':serializer.data, 'message':'Muvafaqqiyatli yangilandi'})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    permission_classes = [permissions.IsAuthenticated, IsUser, ]
    def patch(self, request, pk):
        try:
            gul = self.get_queryset(pk=pk)
        except GullarSerializer.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Bunday soat topilmadi'})
        serializer = GullarSerializer(gul, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'data':serializer.data, 'message':'Muvaffaqiyatli yangilandi'})
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'error':serializer.errors})

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, pk):
        try:
            gul = self.get_object(pk=pk)
        except Gullar.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message':'Bunday soat topilmadi'})
        gul.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'soat muvaffaqiyatli ochirildi'})

