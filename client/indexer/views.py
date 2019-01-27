# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse,Http404,HttpResponse
import file_indexer
from Conf import Configuration
import mimetypes
import os
# Create your views here.

from django.core.files.base import ContentFile

def check(request):

    if request.method =='GET':
        print("ping")
        req_id = request.GET.get('device')
        client_id =  Configuration.get_client_id()
        if not client_id:
            Configuration.set_client_id(req_id)
            client_id = req_id
        if req_id != client_id:
            message = {'message':'client_id is not matching'}
            response = JsonResponse(message)
            response.status_code = 400
            return response
        else:
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

def get_content_url(request):

    if request.method =='GET':
        file =  request.GET.get('file')
        ip = Configuration.get_ip_address()
        path = 'http://'+ip+':8000/getcontent/?file='+file
        result = {'path':path}
        return JsonResponse(result)


def get_content(request):
    if request.method =='GET':
        file_name = request.GET.get('file')
        #print(file_name)
        # file_to_send = ContentFile(file_name)
        # print(file_to_send)
        # content_type = 'application/x-pdf'
        
        # if not file_to_send:
        #     response = HttpResponse(file_to_send,content_type)
        #     response['Content-Length']      = file_to_send.size    
        #     response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        #     return response
        # else:
        #     response = HttpResponse()
        #     response.status_code = 405
        #     return response
                 
        #def serve_using_django_in_memory(request, filename):
        #file_full_path = "/tmp/{0}".format(filename)

        with open(file_name,'r') as f:
            data = f.read()

        response = HttpResponse(data, content_type=mimetypes.guess_type(file_name)[0])
        response['Content-Disposition'] = "attachment; filename={0}".format(file_name)
        response['Content-Length'] = os.path.getsize(file_name)
        return response    
        
