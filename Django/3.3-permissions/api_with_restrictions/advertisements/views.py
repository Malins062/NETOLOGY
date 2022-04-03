from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response

from advertisements.settings import _OPEN, _DRAFT
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite, FavoritePosition
from advertisements.paginations import PagePagination
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AdvertisementFilter

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    pagination_class = PagePagination

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        return []

    def get_queryset(self):
        """
        Получение и фильтрация данных, взависимости от аунтетифицированного пользователя.
        Например, для черновиков объявлений.
        """

        if self.request.user.is_anonymous:
            queryset = Advertisement.objects.exclude(status=_DRAFT)

        elif self.request.user.is_superuser:
            queryset = Advertisement.objects.all()

        else:
            queryset = Advertisement.objects.exclude(~Q(creator=self.request.user), status=_DRAFT)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Вывод списка отфильтрованных объявлений
        """

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        result = [x.values()[0] for x in serializer.data]
        return Response(result)

    @action(detail=False, methods=['get'],
            name="Get favorites advertisements for user")
    def favorites(self, request):
        """
        Вывод объявлений, добавленных в избранное для пользователя
        """
        if self.request.user.is_anonymous:
            return Response({'detail': 'Доступно только для аутентифицированных пользователей'})

        favorites = Advertisement.objects.prefetch_related('favorites').filter(favorites__user=request.user)

        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        """
        Добавление объявления в избранное к пользователю
        """
        advertisement = self.get_object()
        if advertisement.creator == request.user:
            return Response({'detail': 'Вы являетесь автором объявления! '
                                       'В избранное можно добавить только чужие объявления'})

        if advertisement.status == _OPEN:
            instance, created = Favorite.objects.update_or_create(user=request.user,
                                                                  defaults={'user': request.user})
            position, created = FavoritePosition.objects.update_or_create(user=instance, advertisement=advertisement,
                                                                          defaults={'advertisement': advertisement})
            text = 'добавлено в избранное для' if created else 'уже в избранном y'
            return Response({'detail': f'{advertisement} - {text} пользователя {request.user}.'})
        else:
            return Response({'detail': f'{advertisement} - не добавлено в избранное т.к. имеет статус '
                                       f'{advertisement.status}.'})

    @action(detail=True, methods=['delete'])
    def del_favorite(self, request, pk=None):
        """
        Удаление объявления из избранного у пользователя
        """
        advertisement = self.get_object()

        instance = Favorite.objects.get(user=request.user)
        position = FavoritePosition.objects.filter(advertisement=advertisement, user=instance)
        if position:
            position.delete()
            return Response({'detail': f'{advertisement} - объявление удалено из избранного у пользователя '
                                       f'{request.user}.'})
        else:
            return Response({'detail': f'{advertisement} - объявление в избранном у пользователя '
                                       f'{request.user} не найдено.'})

        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
