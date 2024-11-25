from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
