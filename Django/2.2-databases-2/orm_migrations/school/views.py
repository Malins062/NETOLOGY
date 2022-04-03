from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'

    content = Student.objects.all().prefetch_related('teachers').order_by('group')

    context = {
        'object_list': content
    }

    return render(request, template, context)
