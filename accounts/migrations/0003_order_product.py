# Generated by Django 3.0 on 2021-01-06 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210106_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('price', models.FloatField(null=True)),
                ('category', models.CharField(choices=[('Sports', 'Sports'), ('Decor', 'Decor'), ('Food', 'Food')], max_length=250, null=True)),
                ('details', models.TextField()),
                ('date_created', models.DateField(auto_now=True, null=True)),
            ],
        ),
    ]
