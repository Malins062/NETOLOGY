from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from advertisements.models import Advertisement, Favorite, FavoritePosition


class FavoritePositionInlineFormset(BaseInlineFormSet):
    def clean(self):
        advs = set()
        count_forms = 0
        for form in self.forms:
            adv = form.cleaned_data.get('advertisement')
            if adv and form.cleaned_data['DELETE'] is False:
                if self.instance.user == adv.creator:
                    raise ValidationError(f'Ошибка: владелец объявления "{self.instance.user}" '
                                          f'не может добавлять свое объявление "{adv}" '
                                          f'в избранное себе!')
                advs.add(adv.id)
                count_forms += 1

        if len(advs) != count_forms:
            raise ValidationError(f'Имеются дубликаты объявлений в избранном!')

        return super().clean()


class FavoritePositionInline(admin.TabularInline):
    model = FavoritePosition
    formset = FavoritePositionInlineFormset

    extra = 3


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at',
                    'show_favorite_for_users']
    list_filter = ['title', 'description', 'status', 'creator', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'status', 'creator', 'created_at', 'updated_at']

    def show_favorite_for_users(self, obj):
        return ', '.join([a.user.username for a in obj.favorites.all()])
    show_favorite_for_users.short_description = 'В избранном у пользователей'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'show_advertisements_for_user', ]
    list_filter = ['user', ]
    search_fields = ['user']
    inlines = [FavoritePositionInline, ]

    def show_advertisements_for_user(self, obj):
        return ', '.join([f'"{a.id}: {a.title}"' for a in obj.advertisements.all()])
    show_advertisements_for_user.short_description = 'Избранные объявления'
