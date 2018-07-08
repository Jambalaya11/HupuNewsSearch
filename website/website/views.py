#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from settings import STATIC_ROOT
from elasticsearch import Elasticsearch
es = Elasticsearch()

def home(request):
    return render(request, 'index.html', {})


def show_demo(request):
	context = {}
	return render(request, 'demo.html', context)

@csrf_exempt
def get_search_result(request):
	context = {"newstitle":[],"newsurl":[],"content":[],"teamname":[],"teamurl":[],"imageurl":[]}
	query = request.POST.get("query", "")
	body = {
	    "query":{
	        "term":{
	            "teamname":query
	        }
	    }
	}
	result = es.search(index="hupu",doc_type="doc",body=body)
	for item in result["hits"]["hits"]:
		res = item['_source']
		print res
		context['newstitle'].append(res['newstitle'])
		context['newsurl'].append(res['newsurl'])
		context['content'].append(res['content'])
		context['teamname'].append(res['teamname'])
		context['teamurl'].append(res['teamurl'])
		context['imageurl'].append(res['imageurl'])
	return HttpResponse(json.dumps(context))

