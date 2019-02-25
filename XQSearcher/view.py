# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template
from . import getBing

def form_submit(request): 
	request.encoding='utf-8' 
	# 如果GET方法里面有'name' 
	if 'wd' in request.POST: 
		pass
	else: 
		#message = request.POST
		pass
	print(request.POST)

	return HttpResponse(message)

def form_view(request):
	Image = getBing.getImageUrl()
	template = get_template('index.html')
	html = template.render({'Image':Image})
	return HttpResponse(html)

def search(request):
	request.encoding='utf-8'
	template = get_template('search.html')
	print(request.GET)
	if 'wd' in request.GET: 
		html = template.render({'kwd':request.GET['wd']})
		if request.GET['wd'] == '':
			return render_to_response('index.html')
	elif 'bk' in request.GET:
		return render_to_response('index.html')
	else:
		return render_to_response('index.html')
	return HttpResponse(html)

def search_reg(request,wd,page):
	return HttpResponse('wd='+wd+'$page='+page)
