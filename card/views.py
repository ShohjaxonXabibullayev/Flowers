from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from gullar.models import Gullar
from .serializers import CardSerializer, CardItemSerializer
from .models import CardItem, Card
from account.user_perm import IsUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class CardCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class AddToCard(APIView):
    permission_classes = [IsUser, ]
    def post(self, request):
        product_id = request.data['product_id']
        amount = int(request.data['amount'])

        if not Gullar.objects.filter(id=product_id).exists():
            data = {'error':'Siz mavjud bolmagan gulni tanladingiz',
                    'status':status.HTTP_400_BAD_REQUEST}

            return Response(data)
        if amount <= 0 or amount > 100:
            data = {'error':'Siz xato malumot kiritdingiz',
                    'status':status.HTTP_400_BAD_REQUEST}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        card, _ = Card.objects.get_or_create(user=request.user)

        gul = Gullar.objects.get(id=product_id)

        if not CardItem.objects.filter(card=card, product=gul).exists():
            gul = CardItem.objects.create(
                card=card,
                product=gul,
                amount=amount
            )
        else:
            gul = CardItem.objects.get(product=gul)
            gul.amount += amount

        gul.save()

        serializer = CardItemSerializer(gul)
        data = {'data': serializer.data,
                'status': status.HTTP_201_CREATED}
        return Response(data)

class CardItemUpdate(APIView):
    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)

        product = CardItem.objects.get(card__user=request.user, id=pk)
        if count:
            product.amount = int(count)
            product.save()

        elif mtd:
            if mtd == '+':
                product.amount += 1
            elif mtd == '-':
                if product.amount == 1:
                    product.delete()
                else:
                    product.amount -= 1
            product.save()


        else:
            return Response({'error':'Error', 'status':status.HTTP_400_BAD_REQUEST})

        serializer = CardSerializer(product)
        data = {
            'data':serializer.data,
            'status':status.HTTP_200_OK,
            'msg': "O'zgartitldi!"
        }
        return Response(data)



