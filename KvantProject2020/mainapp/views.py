from django.shortcuts import render
from urllib.request import urlopen
import re
from . import models


def parse():
    title_list = []
    url = urlopen('https://www.citilink.ru/search/?text=%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D1%80%D1%8B')
    html = url.read().decode('UTF-8')
    regex = '<span class="image_container"></span>(.*)&nbsp;(.*)\s{16}</a>'
    price_list = re.findall(regex, html)
    for i in price_list:
        title = i[0] + ' ' + i[1]
        title_list.append(title)
    for title in title_list:
        try:
            models.Processor.objects.get(title=title)
        except:
            models.Processor.objects.create_unit(title=title)


def index(request):
    parse()
    context = {

    }
    return render(request, "index.html", context)


def processor_list(request):
    all_processors = models.Processor.objects.all()
    context = {
        'processors': all_processors

    }
    return render(request, "processorList.html", context)


def results(request):
    search = request.GET.get('search', '')
    processors = models.Processor.objects.filter(title__icontains=search)
    context = {
        'processsors': processors

    }
    return render(request, "results.html", context)