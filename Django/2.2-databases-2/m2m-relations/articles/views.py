from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'

    content = Article.objects.all().prefetch_related('scopes')

    context = {
        'object_list': content
    }

    return render(request, template, context)
