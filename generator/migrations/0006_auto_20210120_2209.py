# Generated by Django 3.1.4 on 2021-01-20 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0005_auto_20210120_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='range_from',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='column',
            name='range_to',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='To'),
        ),
    ]
