from rest_framework.pagination import CursorPagination
from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    content = Book.objects.all().order_by('pub_date')
    context = {
        'books': content
    }
    return render(request, template, context)


def books_for_pubdate(request, pub_date):
    template = 'books/books_list.html'

    # qs = Book.objects.all()
    # page_size = 1
    # after = None
    # paginator = CursorPagination(cursor_query_param=qs, ordering='-pub_date')
    # page = paginator.page(first=page_size, after=after)
    # context = {
    #     'books': [p for p in page],
    #     'has_next_page': page.has_next,
    #     'last_cursor': paginator.cursor(page[-1])
    # }

    # content = Book.objects.all().order_by('pub_date')
    # # content = Book.objects.all().values('pub_date').group_by('pub_date')
    #
    # page_number = pub_date
    # paginator = Paginator(content, 1)
    # page = paginator.get_page(page_number)
    #
    # content = Book.objects.get(pub_date=pub_date)
    # context = {
    #     'books': content,
    #     'page': page
    # }

    return render(request, template, context)
