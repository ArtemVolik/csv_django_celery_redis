# Generated by Django 3.1.4 on 2021-01-20 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_auto_20210120_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='schema',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='generator.schema'),
            preserve_default=False,
        ),
    ]
