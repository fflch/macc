from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline
from django.db.models import F


from .models import OriginalFragment, Work


def index(request):
    qs = Work.objects.prefetch_related('translation_set').all()
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


def detail(request, pk: int):
    context = {
        'work': Work.objects.prefetch_related('originalfragment_set').get(pk=pk)
    }

    return render(request, 'corpus/detail.html', context)


def search(request):
    search_pt = True if request.POST.get('search-pt') else False
    search_en = True if request.POST.get('search-en') else False
    phrase = True if request.POST.get('phrase') else False
    q = request.POST.get('q')

    context = {}
    if request.POST:
        context['q'] = q
        if phrase:
            context['phrase'] = 'on'
        search_columns = []

        if search_pt:
            context['search_pt'] = 'on'
            search_columns.append('fragment')
        if search_en:
            context['search_en'] = 'on'
            search_columns.append('translatedfragment__fragment')

        search_vector = SearchVector(*search_columns)
        search_query = SearchQuery(
            q, search_type='phrase' if phrase else 'plain')

        qs = (OriginalFragment.objects
              .annotate(search=search_vector)
              .filter(search=search_query)
              )

        qs = qs.annotate(
            headline_original=SearchHeadline(
                'fragment',
                search_query if search_pt else '',
                start_sel='<strong>',
                stop_sel='</strong>',
                min_words=1000,
                max_words=10000)
        )
        qs = qs.annotate(
            headline_translation=SearchHeadline('translatedfragment__fragment',
                                                search_query if search_en else '',
                                                start_sel='<strong>',
                                                stop_sel='</strong>',
                                                min_words=1000,
                                                max_words=10000),
            translation_code=F('translatedfragment__work__code'),
        )

        context['result'] = qs

    return render(request, 'corpus/search.html', context)
