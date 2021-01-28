from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Separator(models.TextChoices):
    comma = ',', _('Comma (,)')
    semicolon = ';', _('Semicolon (;)')


class Character(models.TextChoices):
    double = '\"', _('Double quote (")')
    single = '\'', _("Single quote (')")


class DataType(models.TextChoices):
    full_name = 'f_n', _('Full name')
    job = 'j', _('Job')
    email = 'e', _('Email')
    company_name = 'c_n', _('Company name')
    integer = 'i', _('Integer')
    date = 'd', _('Date')


class Schema(models.Model):
    name = models.CharField('Name', max_length=50)
    modified = models.DateTimeField(
        verbose_name='Modification date', default=timezone.now)
    user = models.ForeignKey(User,
                             related_name='schemas',
                             on_delete=models.CASCADE)
    column_separator = models.CharField(
        'Column separator', max_length=1,
        choices=Separator.choices)
    string_character = models.CharField(
        'String character', max_length=1,
        choices=Character.choices)


class Column(models.Model):
    name = models.CharField('Name', max_length=50)
    type = models.CharField(max_length=3,
                            choices=DataType.choices,
                            default=DataType.full_name)
    order = models.PositiveIntegerField(verbose_name='Order', default=0)
    range_from = models.PositiveIntegerField('From', blank=True, null=True)
    range_to = models.PositiveIntegerField('To', blank=True, null=True)
    schema = models.ForeignKey(Schema,
                               related_name='columns',
                               on_delete=models.CASCADE)


class Dataset(models.Model):
    created = models.DateTimeField('Created', default=timezone.now)
    status = models.BooleanField("Status", default=False)
    file = models.FileField("CSV file")
    schema = models.ForeignKey(Schema,
                               related_name='datasets',
                               on_delete=models.CASCADE,
                               null=True)

