from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorite
from advertisements.settings import MAX_COUNT, _OPEN, _DRAFT, _CLOSED


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def validate(self, attrs):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.partial and self.context['request'].user.is_superuser:
            attrs['creator'] = self.instance.creator
        else:
            attrs['creator'] = self.context['request'].user

        if attrs.get('status') == _CLOSED or attrs.get('status') == _DRAFT:
            return attrs

        count_opened = Advertisement.objects.filter(creator=attrs['creator'], status=_OPEN).count()
        if count_opened >= MAX_COUNT:
            raise ValidationError(f'У пользователя - {attrs["creator"]}, '
                                  f'не может быть более {MAX_COUNT} открытых объявлений!')
        else:
            return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявлений."""

    class Meta:
        model = Favorite
        fields = '__all__'
