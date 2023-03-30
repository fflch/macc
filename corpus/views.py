from django.http import QueryDict
from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline
from django.contrib import messages
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import OriginalFragment, Work
from .forms import SearchCorpusForm


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
    form = SearchCorpusForm(request.GET or None)

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                label = form.fields[field].label
                messages.error(request, f"{label}: {error}")

        return render(request, 'corpus/search.html', {'form': form})

    search_languages = form.cleaned_data['language']

    search_columns = []
    if 'pt' in search_languages:
        search_columns.append('fragment')
    if 'en' in search_languages:
        search_columns.append('translatedfragment__fragment')

    q = form.cleaned_data['query']

    queryset = (OriginalFragment
                .objects
                .prefetch_related('translatedfragment_set')
                .all())

    match form.cleaned_data['search_type']:
        case 'broad':
            search_vector = SearchVector(*search_columns)
            search_query = SearchQuery(q)
            queryset = queryset.annotate(search=search_vector).filter(
                search=search_query)
        case 'exact':
            filters = [{f'{col}__iregex': fr'\y{q}\y'}
                       for col in search_columns]
            queries = [Q(**args) for args in filters]
            qs_filter = reduce(Q.__or__, queries)
            queryset = queryset.filter(qs_filter)
        case 'start':
            filters = [{f'{col}__iregex': fr'\y{q}'}
                       for col in search_columns]
            queries = [Q(**args) for args in filters]
            qs_filter = reduce(Q.__or__, queries)
            queryset = queryset.filter(qs_filter)
        case 'end':
            filters = [{f'{col}__iregex': fr'{q}\y'}
                       for col in search_columns]
            queries = [Q(**args) for args in filters]
            qs_filter = reduce(Q.__or__, queries)
            queryset = queryset.filter(qs_filter)
        case _: pass

    queryset = queryset.annotate(
        headline_original=SearchHeadline(
            'fragment',
            SearchQuery(q) if 'pt' in search_languages else '',
            start_sel='<strong>',
            stop_sel='</strong>',
            min_words=1000,
            max_words=10000)
    )
    queryset = queryset.annotate(
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

    context = {'form': form}
    paginator = None
    page = None
    if queryset:
        paginator = Paginator(queryset, 10)
    if paginator:
        page = paginator.get_page(request.GET.get('page'))
        context['result'] = page
        context['qs'] = {}

        if page.has_previous():
            first_page_qs = QueryDict(request.GET.urlencode(), mutable=True)
            try:
                first_page_qs.pop('page')
            except KeyError:
                pass
            first_page_qs.update({'page': 1})
            context['qs']['first_page'] = first_page_qs.urlencode()

            previous_page_qs = QueryDict(request.GET.urlencode(), mutable=True)
            try:
                previous_page_qs.pop('page')
            except KeyError:
                pass
            previous_page_qs.update({'page': page.previous_page_number()})
            context['qs']['previous_page'] = previous_page_qs.urlencode()

        if page.has_next():
            next_page_qs = QueryDict(request.GET.urlencode(), mutable=True)
            try:
                next_page_qs.pop('page')
            except KeyError:
                pass
            next_page_qs.update({'page': page.next_page_number()})
            context['qs']['next_page'] = next_page_qs.urlencode()

            last_page_qs = QueryDict(request.GET.urlencode(), mutable=True)
            try:
                last_page_qs.pop('page')
            except KeyError:
                pass
            last_page_qs.update({'page': paginator.num_pages})
            context['qs']['last_page'] = last_page_qs.urlencode()

    return render(request, 'corpus/search.html', context)
