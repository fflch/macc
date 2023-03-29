from django.http import QueryDict
from django.shortcuts import render
from corpus.models import Translation, Collection, Work
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.contrib import messages
from catalogue.forms import SearchEnglishForm, SearchPortugueseForm
from django.core.paginator import Paginator

from logging import getLogger

logger = getLogger(__name__)


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
    romances_qs = (
        Translation
        .objects
        .novels()
        .select_related('publisher', 'publisher__place')
        .prefetch_related('authors')
        .only(
            'code',
            'year',
            'title',
            'authors',
            'publisher__name',
            'publisher__place__city',
            'publisher__place__country',
        )
        .annotate(
            title_portuguese=F('work__title'),
            title_english=F('title'),
            publisher_name=F('publisher__name'),
            place_name=Concat(
                F('publisher__place__city'),
                Value(' - '),
                F('publisher__place__country'),
            ),
            country=F('publisher__place__country'),
        )
    )

    collections_qs = (
        Collection
        .objects
        .all()
        .select_related('publisher', 'publisher__place')
        .prefetch_related('authors')
        .only(
            'code',
            'year',
            'title',
            'authors',
            'publisher__name',
            'publisher__place__city',
            'publisher__place__country',
        )
        .annotate(
            title_portuguese=Value(''),
            title_english=F('title'),
            publisher_name=F('publisher__name'),
            place_name=Concat(
                F('publisher__place__city'),
                Value(' - '),
                F('publisher__place__country'),
            ),
            country=F('publisher__place__country'),
        )
    )

    form = SearchEnglishForm(request.GET)
    queryset = None

    if form.is_valid():
        if form.cleaned_data['year_from']:
            romances_qs = romances_qs.filter(
                year__gte=int(form.cleaned_data['year_from']))
            collections_qs = collections_qs.filter(
                year__gte=int(form.cleaned_data['year_from']))
        if form.cleaned_data['year_until']:
            romances_qs = romances_qs.filter(
                year__lte=int(form.cleaned_data['year_until']))
            collections_qs = collections_qs.filter(
                year__lte=int(form.cleaned_data['year_until']))
        if form.cleaned_data['title_portuguese']:
            romances_qs = romances_qs.filter(
                title_portuguese__icontains=form.cleaned_data['title_portuguese'])
            collections_qs = collections_qs.filter(
                title_portuguese__icontains=form.cleaned_data['title_portuguese'])
        if form.cleaned_data['title_english']:
            romances_qs = romances_qs.filter(
                title_english__icontains=form.cleaned_data['title_english'])
            collections_qs = collections_qs.filter(
                title_english__icontains=form.cleaned_data['title_english'])
        if form.cleaned_data['gender']:
            for gender in form.cleaned_data['gender']:
                romances_qs = romances_qs.filter(code__icontains=gender)
                collections_qs = collections_qs.filter(
                    code__icontains=gender)
        if form.cleaned_data['country']:
            romances_qs = romances_qs.filter(
                country__in=form.cleaned_data['country'])
            collections_qs = collections_qs.filter(
                country__in=form.cleaned_data['country'])
        queryset = romances_qs.union(collections_qs).order_by('year')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                label = form.fields[field].label
                messages.error(request, f"{label}: {error}")

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

    return render(request, f'catalogue/search_english.html', context)


def search_portuguese(request):
    queryset = (Work
                .objects
                .prefetch_related('translation_set')
                .filter(translation__id__isnull=False)
                .distinct()
                .order_by('year'))

    form = SearchEnglishForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['title_portuguese']:
            queryset = queryset.filter(
                title__icontains=form.cleaned_data['title_portuguese'])
        if form.cleaned_data['gender']:
            for gender in form.cleaned_data['gender']:
                queryset = queryset.filter(code__icontains=gender)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                label = form.fields[field].label
                messages.error(request, f"{label}: {error}")

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

    return render(request, f'catalogue/search_portuguese.html', context)


def show(request, code):
    return render(request, f'catalogue/{code}.html')
