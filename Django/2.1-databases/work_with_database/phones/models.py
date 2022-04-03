from django.db import models


class Phone(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    image = models.URLField(null=True)
    price = models.IntegerField(default=0)
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
