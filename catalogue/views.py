from django.shortcuts import render
from corpus.models import Translation, Collection


def timeline(request):
    qs = (Translation
          .objects
          .novels()
          .only('code', 'title', 'year')
          ).union(
        Collection
        .objects
        .all()
        .only('code', 'title', 'year')).order_by('year')

    return render(request, f'catalogue/timeline.html', {'result': qs})


def search_english(request):
    return render(request, f'catalogue/search_english.html')


def search_portuguese(request):
    return render(request, f'catalogue/search_portuguese.html')


def show(request, code):
    return render(request, f'catalogue/{code}.html')
