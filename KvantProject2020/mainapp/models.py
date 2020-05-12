from django.db import models


class Manufacturer(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} {self.title}'


class ProcessorManager(models.Manager):
    def create_unit(self, title, link, price, image):
        processor = self.create(title=title, link=link, price=price, image=image)
        return processor


class GPUManager(models.Manager):
    def create_unit(self, GPU_Name, GPULink):
        gpu = self.create(GPU_Name=GPU_Name, GPULink=GPULink)
        return gpu


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

    objects = ProcessorManager()

    def __str__(self):
        return f'{self.id} {self.title}'


class GPU(models.Model):
    id = models.BigAutoField(primary_key=True)
    GPU_Name = models.CharField(max_length=150)
    GPU_Price = models.IntegerField(default=0)
    GPUImage = models.ImageField(upload_to='static/images', default='ne zavezli')
    GPU_Annotation = models.CharField(max_length=1000)
    videoMemory = models.CharField(max_length=150)
    typeOfVideoMemory = models.CharField(max_length=150)
    addPower = models.BooleanField(default=False)
    GPULink = models.CharField(max_length=150, default='ne zavezli')
    gpuObjects = GPUManager()

    def __str__(self):
        return f'{self.id} {self.GPU_Name}'

