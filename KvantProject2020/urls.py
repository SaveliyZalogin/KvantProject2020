"""KvantProject2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from .mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('processors/', views.processor_list, name='processors'),
    path('gpus/', views.gpu_list, name='gpus'),
    path('results/', views.results, name='results'),
    re_path(r'^processor/(?P<processor_id>\d+)$', views.processor, name="processor"),
    re_path(r'^videokarta/(?P<gpu_id>\d+)$', views.gpu, name="gpu"),
]
