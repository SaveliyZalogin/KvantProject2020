from django.shortcuts import render
from urllib.request import urlopen
import re
from . import models
import time
from bs4 import BeautifulSoup
import requests


def parce_processor_properties(processor):
    result = ''
    processors = models.Processor.objects.all()
    html = ''
    link_list = []
    for link in processors:
        link_list.append(link.link)
    for i in link_list:
        if i == processor.link:
            r = requests.get(str(i))
            soup = BeautifulSoup(r.content, 'lxml')
            annotation = soup.find('p', class_="short_description")
            result = annotation.get_text()
    return result


def parse():
    old_price = []
    r = requests.get('https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/')
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.find_all('a', class_="link_gtm-js link_pageevents-js ddl_product_link")
    price = soup.find_all('ins', class_="subcategory-product-item__price-num")
    link = soup.find_all('a', class_="link_gtm-js link_pageevents-js ddl_product_link")
    image = soup.find_all('img', class_="product-card__img lazyload")
    print(image)
    print(len(name))
    for i in range(0, len(name)):
        title = name[i].get_text()
        finalPrice = price[i].get_text()
        finalLink = link[i].get('href')
        finalImage = image[i].get('data-src')
        print(finalImage)
        try:
            models.Processor.objects.get(title=title, link=finalLink, price=finalPrice, image=finalImage)
        except:
            models.Processor.objects.create_unit(title=title, link=finalLink, price=finalPrice, image=finalImage)
# def parse():
#     title = ''
#     link = ''
#     a = 0
#     url = urlopen('https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/')
#     html = url.read().decode('UTF-8')
#     regex_link = '<div class="wrap-img"><a href="(.*)"'
#     link_list = re.findall(regex_link, html)
#     regex_title = '<span class="image_container"></span>(.*)&nbsp;(.*)\s{16}</a>'
#     # regex_annotation = '<p class="short_description">(.*)&nbsp;&#151;\s(.*)&nbsp;&#151;\s(.*)&nbsp;&#151;\s(.*)</p>'
#     title_list = re.findall(regex_title, html)
#     print(len(title_list))
#     print(len(link_list))
#     link_list.remove('https://www.citilink.ru/catalog/computers_and_notebooks/parts/cpu/1067853/')
#     for c in range(0, len(title_list)):
#         b = title_list[c]
#         title = b[0] + ' ' + b[1]
#         m = link_list[c]
#         link = m
#         try:
#             models.Processor.objects.get(title=title, link=link)
#         except:
#             models.Processor.objects.create_unit(title=title, link=link)
            models.Processor.objects.create_unit(title=title, link=finalLink, price=finalPrice)


def index(request):
    context = {

    }
    return render(request, "index.html", context)


def processor_list(request):
    all_processors = models.Processor.objects.all()
    parse()
    context = {
        'processors': all_processors,
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
    properties = parce_processor_properties(processor)
    context = {
        'processor': processor,
        'properties': properties,
    }
    return render(request, "processor.html", context)