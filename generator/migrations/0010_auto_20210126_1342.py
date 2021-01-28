# Generated by Django 3.1.4 on 2021-01-26 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0009_dataset_schema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='file',
            field=models.FileField(upload_to='csv', verbose_name='CSV file'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='schema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to='generator.schema'),
        ),
    ]