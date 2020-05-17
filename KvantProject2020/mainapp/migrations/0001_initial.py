# Generated by Django 3.0.5 on 2020-04-30 11:20

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GPU',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('GPU_Name', models.CharField(max_length=150)),
                ('GPU_Annotation', models.CharField(max_length=1000)),
                ('videoMemory', models.CharField(max_length=150)),
                ('typeOfVideoMemory', models.CharField(max_length=150)),
                ('addPower', models.BooleanField(default=False)),
            ],
            managers=[
                ('gpuObjects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('link', models.CharField(blank=True, max_length=200)),
                ('image', models.CharField(default='Image', max_length=500)),
                ('price', models.CharField(default='0', max_length=50)),
                ('annotation', models.CharField(max_length=1000)),
                ('socket', models.CharField(max_length=50)),
                ('threads', models.IntegerField(default=0)),
                ('cache', models.CharField(max_length=20)),
                ('frequency', models.CharField(max_length=50)),
                ('TDP', models.CharField(max_length=50)),
            ],
        ),
    ]