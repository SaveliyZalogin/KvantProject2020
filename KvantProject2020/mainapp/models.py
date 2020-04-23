from django.db import models


class ProcessorManager(models.Manager):
    def create_unit(self, title, link):
        processor = self.create(title=title, link=link)
        return processor


class Processor(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=200, blank=True)
    image = models.CharField(max_length=500, default='Image')
    price = models.IntegerField
    annotation = models.CharField(max_length=1000)
    socket = models.CharField(max_length=50)
    threads = models.IntegerField
    cache = models.CharField(max_length=20)
    frequency = models.CharField(max_length=50)
    TDP = models.CharField(max_length=50)

    objects = ProcessorManager()

    def __str__(self):
        return f'{self.id} {self.title}'
