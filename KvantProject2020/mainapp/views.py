from django.shortcuts import render
from urllib.request import urlopen
import re
from . import models
import time
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponseRedirect
import random


def parce_processor_properties(element):
    result = ''
    processors = models.Processor.objects.all()
    gpus = models.GPU.objects.all()
    motherboards = models.Motherboard.objects.all()
    html = ''
    link_list = []
    for link in processors:
        link_list.append(link.link)
    for link in gpus:
        link_list.append(link.link)
    for link in motherboards:
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
    motherboards = models.Motherboard.objects.all()
    if len(processors) == 0 or len(gpus) == 0 or len(motherboards) == 0:
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
            categorymth = re.findall(r'categoryName&quot;:&quot;(\w*)&quot;,', finalall)
            brand = re.findall(r'"brandName":"(.*)",', finalall)
            print(finalall)
            print(finalImage)
            print(category)
            if category[0] == 'Процессоры':
                try:
                    models.Processor.objects.get(title=fnTitle[0],
                                                 link=finalLink,
                                                 price=fnPrice[0],
                                                 image=finalImage,
                                                 brand_name=brand[0])
                except:
                    models.Processor.objects.create_unit(title=fnTitle[0],
                                                         link=finalLink,
                                                         price=fnPrice[0],
                                                         image=finalImage,
                                                         brand=brand[0])
            elif category[0] == 'Видеокарты':
                try:
                    models.GPU.objects.get(title=fnTitle[0],
                                           link=finalLink,
                                           price=fnPrice[0],
                                           image=finalImage,
                                           brand=brand[0])
                except:
                    models.GPU.objects.create_unit(title=fnTitle[0],
                                                   link=finalLink,
                                                   price=fnPrice[0],
                                                   image=finalImage,
                                                   brand=brand[0])
            elif categorymth[0] == 'Материнские платы':
                try:
                    models.Motherboard.objects.get(title=fnTitle[0],
                                                   link=finalLink,
                                                   price=fnPrice[0],
                                                   image=finalImage,
                                                   brand=brand[0])
                except:
                    models.Motherboard.objects.create_unit(title=fnTitle[0],
                                                           link=finalLink,
                                                           price=fnPrice[0],
                                                           image=finalImage,
                                                           brand=brand[0])


def index(request):
    processors = models.Processor.objects.all()
    gpus = models.GPU.objects.all()
    motherboards = models.Motherboard.objects.all()
    resultprc = random.choice(processors)
    resultgpu = random.choice(gpus)
    resultmth = random.choice(motherboards)
    context = {
        'prc': resultprc,
        'gpu': resultgpu,
        'mth': resultmth,
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
    brand_gpu_query = []
    all_gpus = models.GPU.objects.all()
    for gpu in all_gpus:
        if gpu.brand_name not in brand_gpu_query:
            brand_gpu_query.append(gpu.brand_name)
    parse('https://bit.ly/2WaZ1QO')
    context = {
        'gpus': all_gpus,
        'gpu_query': brand_gpu_query,
    }
    return render(request, "gpuList.html", context)


def results(request):
    processors = None
    gpus = None
    postavka = ''
    brand = ''
    search = request.GET.get('search', '')
    getprice = request.GET.get('price', '')
    manufacturer_amd = request.GET.get('manufacturer_amd', '')
    manufacturer_intel = request.GET.get('manufacturer_intel', '')
    manufacturer_msi = request.GET.get('manufacturer_msi', '')
    manufacturer_gigabyte = request.GET.get('manufacturer_gigabyte', '')
    manufacturer_palit = request.GET.get('manufacturer_palit', '')
    manufacturer_asus = request.GET.get('manufacturer_asus', '')
    in_oem = request.GET.get('in_oem', '')
    in_box = request.GET.get('in_box', '')
    if in_oem == 'on':
        postavka = 'OEM'
        processors = models.Processor.objects.filter(title__icontains=postavka)
    elif in_box == 'on':
        postavka = 'BOX'
        processors = models.Processor.objects.filter(title__icontains=postavka)
    if manufacturer_amd == 'on':
        brand = 'AMD'
        processors = models.Processor.objects.filter(brand_name=brand)
    elif manufacturer_intel == 'on':
        brand = 'INTEL'
        processors = models.Processor.objects.filter(brand_name=brand)
    elif manufacturer_msi == 'on':
        brand = 'MSI'
        gpus = models.GPU.objects.filter(brand_name=brand)
    elif manufacturer_gigabyte == 'on':
        brand = 'GIGABYTE'
        gpus = models.GPU.objects.filter(brand_name=brand)
    elif manufacturer_palit == 'on':
        brand = 'PALIT'
        gpus = models.GPU.objects.filter(brand_name=brand)
    elif manufacturer_asus == 'on':
        brand = 'ASUS'
        gpus = models.GPU.objects.filter(brand_name=brand)
    if len(getprice) > 0:
        processors = []
        gpus = []
        m = range(int(getprice) - 1500, int(getprice) + 1500)
        price = m
        for i in m:
            processors += models.Processor.objects.filter(price=i)
            gpus += models.GPU.objects.filter(price=i)
    if len(postavka) > 0 and len(brand) > 0 and len(price) == 0:
        processors = []
        gpus = []
        processors = models.Processor.objects.filter(title__icontains=postavka, brand_name=brand)
        print(len(price))
    elif len(postavka) == 0 and len(brand) > 0 and len(price) > 0:
        processors = []
        gpus = []
        for i in price:
            processors += models.Processor.objects.filter(brand_name=brand, price=i)
            gpus += models.GPU.objects.filter(brand_name=brand, price=i)
    elif len(price) > 0 and len(postavka) > 0 and len(brand) > 0:
        processors = []
        gpus = []
        for i in price:
            processors += models.Processor.objects.filter(title__icontains=postavka, brand_name=brand, price=i)
    if len(search) > 0:
        sprc = re.findall('ПРОЦЕССОР ЗА (\d*)', search.upper())
        sgpu = re.findall('ВИДЕОКАРТА ЗА (\d*)', search.upper())
        if len(sprc) > 0 or len(sgpu) > 0:
            if len(sprc) > 0:
                srchprc = re.findall('ПРОЦЕССОР ЗА (\d*)', search.upper())
                processors = models.Processor.objects.filter(price=srchprc[0])
            elif len(sgpu) > 0:
                srchpgu = re.findall('ВИДЕОКАРТА ЗА (\d*)', search.upper())
                gpus = models.GPU.objects.filter(price=srchpgu[0])
        else:
            processors = models.Processor.objects.filter(title__icontains=search)
            gpus = models.GPU.objects.filter(title__icontains=search)
    if search.upper() == 'ПРОЦЕССОРЫ':
        return HttpResponseRedirect("/processors/")
    elif search.upper() == 'ВИДЕОКАРТЫ':
        return HttpResponseRedirect("/gpus/")
    context = {
        'processsors': processors,
        'gpus': gpus,
        'price': getprice,
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


def motherboards(request):
    motherboards = models.Motherboard.objects.all()
    parse("https://bit.ly/2LrPujh")
    context = {
        'motherboards': motherboards,

    }
    return render(request, "motherboardList.html", context)


def motherboard(request, motherboard_id):
    mthboard = models.Motherboard.objects.get(id=motherboard_id)
    properties = parce_processor_properties(mthboard)
    context = {
        'mthboard': mthboard,
        'properties': properties,
    }
    return render(request, "motherboard.html", context)
