from django.contrib import admin
from .models import Schema, Column, Dataset


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    readonly_fields = ['modified']


admin.site.register(Column)
admin.site.register(Dataset)
