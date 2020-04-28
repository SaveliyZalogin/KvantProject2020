from django.shortcuts import render
import re
from . import models
import time
import requests
from bs4 import BeautifulSoup


def parse():
    r = requests.get('https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/')
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find_all('a', class_="link_gtm-js link_pageevents-js ddl_product_link")
    price = soup.find_all('ins', class_="subcategory-product-item__price-num")
    link = soup.find_all('a', class_="link_gtm-js link_pageevents-js ddl_product_link")

    for i in range(0, len(name)):
        title = name[i].get_text()
        finalPrice = price[i].get_text()
        finalLink = link[i].get('href')
        try:
            models.Processor.objects.get(title=title, link=finalLink, price=finalPrice)
        except:
            models.Processor.objects.create_unit(title=title, link=finalLink, price=finalPrice)




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