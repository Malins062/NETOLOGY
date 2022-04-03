from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class MyPagination(PageNumberPagination):
    page_size = 10


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_set_fields = ['id', 'title', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description']

    pagination_class = MyPagination


class StockSearchFilter(SearchFilter):
    search_param = 'product'


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.prefetch_related('positions').all()
    serializer_class = StockSerializer

    filter_backends = [DjangoFilterBackend, StockSearchFilter, OrderingFilter]
    filterset_fields = ['address', ]
    search_fields = ['address',
                     '=positions__product__id',
                     'positions__product__title',
                     'positions__product__description']
    ordering_fields = ['id', 'address']

    pagination_class = MyPagination
