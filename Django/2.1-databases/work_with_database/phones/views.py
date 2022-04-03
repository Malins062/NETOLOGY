from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    content = Phone.objects.all()

    sort = request.GET.get('sort')
    if sort == 'name':
        content = content.order_by('name')
    elif sort == 'min_price':
        content = content.order_by('price')
    elif sort == 'max_price':
        content = content.order_by('-price')

    context = {
        'phones': content
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'

    content = Phone.objects.filter(slug=slug)

    context = {
        'phone': content[0]
    }
    return render(request, template, context)
