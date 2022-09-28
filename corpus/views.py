from django.shortcuts import render

from .models import Work


def index(request):
    qs = Work.objects.prefetch_related('translation_set').all()
    # qs = Work.objects.all()
    context = {
        'novels': qs.novels(),
        'short_stories': qs.short_stories()
    }

    return render(request, 'corpus/index.html', context)


def show(request, pk: int):
    qs = Work.objects.prefetch_related(
        'translation_set', 'translation_set__authors').all()
    context = {
        'work': qs.get(pk=pk)
    }

    return render(request, 'corpus/show.html', context)


def search(request):
    return render(request, 'corpus/search.html', {})
