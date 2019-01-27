# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import file_indexer

# Create your views here.


def check(request):
    resp = {'message':'pong'}
    return JsonResponse(resp)


def get_indexes(request):

    if request.method=='GET':
        start_time = request.GET.get('from')
        if start_time:
            start_time = long(start_time)
        else:
            start_time = -1
        
        result = file_indexer.get_new_indexing(start_time)
        return JsonResponse(result)

        
