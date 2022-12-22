from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required


from .models import OriginalFragment, Work


from functools import reduce


def index(request):
    qs = (Work
          .objects
          .prefetch_related('translation_set')
          .filter(translation__id__isnull=False)
          .distinct()
          .order_by('id'))
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


@login_required
def search(request):
    search_languages = request.POST.get('search-language', [])

    context = {
        'pt': 'pt' in search_languages,
        'en': 'en' in search_languages,
    }

    search_columns = []
    if 'pt' in search_languages:
        search_columns.append('fragment')
    if 'en' in search_languages:
        search_columns.append('translatedfragment__fragment')

    if request.POST:
        q = request.POST.get('q')

        qs = (OriginalFragment
              .objects
              .prefetch_related('translatedfragment_set')
              .all())

        match request.POST.get('search-method'):
            case 'broad':
                search_vector = SearchVector(*search_columns)
                search_query = SearchQuery(q)
                qs = qs.annotate(search=search_vector).filter(
                    search=search_query)
            case 'exact':
                filters = [{f'{col}__iregex': fr'\y{q}\y'}
                           for col in search_columns]
                queries = [Q(**args) for args in filters]
                qs_filter = reduce(Q.__or__, queries)
                qs = qs.filter(qs_filter)
            case 'start':
                filters = [{f'{col}__iregex': fr'\y{q}'}
                           for col in search_columns]
                queries = [Q(**args) for args in filters]
                qs_filter = reduce(Q.__or__, queries)
                qs = qs.filter(qs_filter)
            case 'end':
                filters = [{f'{col}__iregex': fr'{q}\y'}
                           for col in search_columns]
                queries = [Q(**args) for args in filters]
                qs_filter = reduce(Q.__or__, queries)
                qs = qs.filter(qs_filter)
            case _: pass

        qs = qs.annotate(
            headline_original=SearchHeadline(
                'fragment',
                SearchQuery(q) if 'pt' in search_languages else '',
                start_sel='<strong>',
                stop_sel='</strong>',
                min_words=1000,
                max_words=10000)
        )
        qs = qs.annotate(
            headline_translation=SearchHeadline(
                'translatedfragment__fragment',
                SearchQuery(q)
                if 'en' in search_languages else '',
                start_sel='<strong>',
                stop_sel='</strong>',
                min_words=1000,
                max_words=10000
            ),
            translation_code=F('translatedfragment__work__code'),
        )

        context['result'] = qs

    return render(request, 'corpus/search.html', context)
