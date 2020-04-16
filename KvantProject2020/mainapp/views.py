from django.shortcuts import render
from urllib.request import urlopen
import re
from . import models
import re


def index(request):
    context = {


    }
    return render(request, "index.html", context)


def configurate(request):
    context = {


    }
    return render(request, "filters.html", context)


def results(request):
    sborka = None
    all_results = models.Result.objects.all()
    CPU = ''
    GPU = ''
    list_CPUs = ['Intel Core i5 @12000@', 'AMD Ryzen 5 3600 @16000@', 'Intel Core i7 @20000@']
    list_GPUs = ['Geforce GTX 1060 {18000}', 'Geforce GTX 1660 super {22000}', 'Geforce GTX 2060 super {30000}']
    budget = request.GET.get('budget', '')
    one_piece_of_bdg = int(budget) // 8
    CPU_price = one_piece_of_bdg * 2
    GPU_price = one_piece_of_bdg * 3
    c = []
    for compl in list_CPUs:
        a = re.findall('.*\s*@(\d*)@', compl)
        b = re.findall('(.*\s*)@\d*@', compl)
        if CPU_price - int(a[0]) > -500:
            c.append(CPU_price - int(a[0]))

    for compl in list_GPUs:
        a = re.findall('.*\s*{(\d*)}', compl)
        b = re.findall('(.*\s*){\d*}', compl)
        if int(a[0]) in range(GPU_price - 1250, GPU_price + 1250):
            GPU += str(b[0])
            print(GPU)

    # if int(CPU_price) in range(0, 12000):
    #     CPU += 'Intel Core i5'
    # elif int(CPU_price) in range(0, 20000):
    #     CPU += 'Intel Core i7'
    #
    # if int(GPU_price) in range(15000, 20000):
    #     GPU += 'Geforce GTX 1660 super'
    # elif int(GPU_price) in range(20000, 40000):
    #     GPU += 'Geforce GTX 2060 super'

    try:
        sborka = models.Result.objects.get(price=budget, CPU=CPU, GPU=GPU)
    except:
        result = models.Result.objects.create_result(price=budget, CPU=CPU, GPU=GPU)
        sborka = models.Result.objects.get(price=budget, CPU=CPU, GPU=GPU)

    context = {
        'budget': budget,
        'sborka': sborka,
    }
    return render(request, "results.html", context)