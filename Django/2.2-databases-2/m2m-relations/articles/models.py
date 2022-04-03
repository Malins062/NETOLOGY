from django.db import models


class Article(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Раздел')
    articles = models.ManyToManyField(Article, verbose_name='Статьи', related_name='tags', through='ArticleScope')

    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

    def __str__(self):
        return self.name


class ArticleScope(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел', related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'

    def __str__(self):
        return f'{"Основной раздел" if self.is_main else ""}'
