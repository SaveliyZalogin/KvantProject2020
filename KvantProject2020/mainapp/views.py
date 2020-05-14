from django.shortcuts import render
from urllib.request import urlopen
import re
from . import models
import time
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponseRedirect


def parce_processor_properties(element):
    result = ''
    processors = models.Processor.objects.all()
    gpus = models.GPU.objects.all()
    html = ''
    link_list = []
    for link in processors:
        link_list.append(link.link)
    for link in gpus:
        link_list.append(link.link)
    for i in link_list:
        if i == element.link:
            if len(element.annotation) == 0:
                r = requests.get(str(i))
                soup = BeautifulSoup(r.content, 'lxml')
                annotation = soup.find('p', class_="short_description")
                result = annotation.get_text()
                element.annotation = result
                element.save()
                print(result)
    return result


def parse(product_list_link):
    processors = models.Processor.objects.all()
    gpus = models.GPU.objects.all()
    if len(processors) == 0 or len(gpus) == 0:
        r = requests.get(product_list_link)
        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find_all('a', class_="link_gtm-js link_pageevents-js ddl_product_link")
        price = soup.find_all('div', class_="actions subcategory-product-item__action-container")
        link = soup.find_all('a', class_="link_gtm-js link_pageevents-js ddl_product_link")
        image = soup.find_all('img', class_="lazyload")
        for i in range(3, len(name)):
            title = name[i].get_text()
            finalall = price[i].get('data-params')
            finalLink = link[i].get('href')
            finalImage = image[i - 3].get('data-src')
            fnPrice = re.findall(r'"price":(\d*),', finalall)
            fnTitle = re.findall(r'"shortName":"(.*)","categoryName"', finalall)
            category = re.findall(r'"categoryName":"(\w*)","brandName"', finalall)
            print(finalall)
            print(finalImage)
            print(i)
            if category[0] == 'Процессоры':
                try:
                    models.Processor.objects.get(title=fnTitle[0], link=finalLink, price=fnPrice[0], image=finalImage)
                except:
                    models.Processor.objects.create_unit(title=fnTitle[0], link=finalLink, price=fnPrice[0], image=finalImage)
            else:
                try:
                    models.GPU.objects.get(title=fnTitle[0], link=finalLink, price=fnPrice[0], image=finalImage)
                except:
                    models.GPU.objects.create_unit(title=fnTitle[0], link=finalLink, price=fnPrice[0], image=finalImage)
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
#             models.Processor.objects.create_unit(title=title, link=finalLink, price=finalPrice)


def index(request):
    context = {

    }
    return render(request, "index.html", context)


def processor_list(request):
    all_processors = models.Processor.objects.all()
    parse('https://bit.ly/2VQnLik')
    context = {
        'processors': all_processors,
    }
    return render(request, "processorList.html", context)


def gpu_list(request):
    all_gpus = models.GPU.objects.all()
    parse('https://bit.ly/2WaZ1QO')
    context = {
        'gpus': all_gpus,

    }
    return render(request, "gpuList.html", context)


def results(request):
    search = request.GET.get('search', '')
    processors = models.Processor.objects.filter(title__icontains=search)
    gpus = models.GPU.objects.filter(title__icontains=search)
    if search.upper() == 'ПРОЦЕССОРЫ':
        return HttpResponseRedirect("/processors/")
    elif search.upper() == 'ВИДЕОКАРТЫ':
        return HttpResponseRedirect("/gpus/")
    context = {
        'processsors': processors,
        'gpus': gpus,
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


def gpu(request, gpu_id):
    gpu = models.GPU.objects.get(id=gpu_id)
    properties = parce_processor_properties(gpu)
    context = {
        'videokarta': gpu,
        'properties': properties,
    }
    return render(request, "gpu.html", context)
