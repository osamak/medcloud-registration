# -*- coding: utf-8  -*-
from django import forms
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cloudsearch.utils import search_index


class SearchForm(forms.Form):
    term = forms.CharField(label=u'العبارة', max_length=100)

@csrf_exempt
def search(request):
    if request.method == 'GET':
        if 'term' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                term = form.cleaned_data['term']
                results = search_index(term)
                context = {'form': form, 'results': results, 'term': term}
                return render(request, 'cloudsearch/results.html', context)
            else:
                context = {'form': form}
        else:
            form = SearchForm()
            context = {'form': form}

    return render(request, 'cloudsearch/search.html', context)
