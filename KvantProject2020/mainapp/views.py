from django.shortcuts import render
from urllib.request import urlopen
import re
from . import models
import time


def parse():
    title = ''
    link = ''
    a = 0
    url = urlopen('https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/')
    html = url.read().decode('UTF-8')
    regex_link = '<div class="wrap-img"><a href="(.*)"'
    link_list = re.findall(regex_link, html)
    regex_title = '<span class="image_container"></span>(.*)&nbsp;(.*)\s{16}</a>'
    # regex_annotation = '<p class="short_description">(.*)&nbsp;&#151;\s(.*)&nbsp;&#151;\s(.*)&nbsp;&#151;\s(.*)</p>'
    title_list = re.findall(regex_title, html)
    print(len(title_list))
    print(len(link_list))
    link_list.remove('https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/1067853/')
    for c in range(0, len(title_list)):
        b = title_list[c]
        title = b[0] + ' ' + b[1]
        m = link_list[c]
        link = m
        try:
            models.Processor.objects.get(title=title, link=link)
        except:
            models.Processor.objects.create_unit(title=title, link=link)


def index(request):
    context = {

    }
    return render(request, "index.html", context)


def processor_list(request):
    all_processors = models.Processor.objects.all()
    parse()
    context = {
        'processors': all_processors

    }
    return render(request, "processorList.html", context)


def results(request):
    search = request.GET.get('search', '')
    processors = models.Processor.objects.filter(title__icontains=search)
    context = {
        'processsors': processors,

    }
    return render(request, "results.html", context)


def processor(request, processor_id):
    processor = models.Processor.objects.get(id=processor_id)
    context = {
        'processor': processor,

    }
    return render(request, "processor.html", context)