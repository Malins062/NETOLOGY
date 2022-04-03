from django.conf import settings
from  advertisements.settings import _OPEN, _DRAFT, _CLOSED
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = _OPEN, 'Открыто'
    CLOSED = _CLOSED, 'Закрыто'
    DRAFT = _DRAFT, 'Черновик'


class Advertisement(models.Model):
    """Объявление."""

    id = models.AutoField(unique=True, primary_key=True)
    title = models.TextField(verbose_name='Текст')
    description = models.TextField(default='', verbose_name='Описание')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
        verbose_name='Статус'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создатель'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-updated_at']

    def __str__(self):
        return f'Объявление №{self.id}: {self.title} ({self.creator})'


class Favorite(models.Model):
    """
    Объявления, добавленные в избранное для пользователей.
    """

    # id = models.AutoField(unique=True, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
        unique=True, primary_key=True
    )
    advertisements = models.ManyToManyField(
        Advertisement,
        verbose_name='Избранные объявления',
        related_name='favorites',
        through='FavoritePosition'
    )

    class Meta:
        verbose_name = 'Избранные объявления для пользователя'
        verbose_name_plural = 'Избранные объявления'

    def __str__(self):
        return self.user.get_full_name()


class FavoritePosition(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(
        Favorite,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    advertisement = models.ForeignKey(
        Advertisement,
        verbose_name='Объявления',
        on_delete=models.CASCADE,
        related_name='favorite',

    )
    added_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ссылка на объявление'
        verbose_name_plural = 'Позиции объявлений'

    def __str__(self):
        return f'Добавлено {self.added_at}'
