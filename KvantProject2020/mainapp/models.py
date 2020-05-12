from django.db import models


class Manufacturer(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} {self.title}'


class Manager(models.Manager):
    def create_unit(self, title, link, price, image):
        processor = self.create(title=title, link=link, price=price, image=image)
        return processor


class Processor(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=200, blank=True)
    image = models.CharField(max_length=500, default='Image')
    price = models.CharField(max_length=50, default='0')
    annotation = models.CharField(max_length=1000)
    socket = models.CharField(max_length=50)
    threads = models.IntegerField(default=0)
    cache = models.CharField(max_length=20)
    frequency = models.CharField(max_length=50)
    TDP = models.CharField(max_length=50)

    objects = Manager()

    def __str__(self):
        return f'{self.id} {self.title}'


class GPU(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=200, default='link')
    price = models.CharField(max_length=50, default='price')
    image = models.CharField(max_length=200, default='image')
    annotation = models.CharField(max_length=1000)
    videoMemory = models.CharField(max_length=150)
    typeOfVideoMemory = models.CharField(max_length=150)
    addPower = models.BooleanField(default=False)

    objects = Manager()

    def __str__(self):
        return f'{self.id} {self.title}'

