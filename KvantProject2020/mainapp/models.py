from django.db import models


class ResultManager(models.Manager):
    def create_result(self, price, CPU, GPU):
        result = self.create(price=price, CPU=CPU, GPU=GPU)
        return result


class Result(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.CharField(max_length=10)
    CPU = models.CharField(max_length=150)
    GPU = models.CharField(max_length=150)
    corpus = models.CharField(max_length=150)
    powerblock = models.CharField(max_length=150)
    motherplata = models.CharField(max_length=150)
    ozu = models.CharField(max_length=150)
    HDD = models.CharField(max_length=150, blank=True)
    SSD = models.CharField(max_length=150, blank=True)
    ohlagdenie = models.CharField(max_length=150)

    objects = ResultManager()

    def __str__(self):
        return f'{self.id} {self.price}'
