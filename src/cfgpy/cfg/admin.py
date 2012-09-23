'''
Created on Aug 15, 2012

@author: Alex
'''
from models import DatasetXml
from django.contrib import admin

class DatasetXmlAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields':['name']}),
                 (None, {'fields':['created_by']}),
                 ('Date information', {'fields':['date_created']})]
    list_display = ('name', 'created_by', 'date_created')
    list_filter = ['date_created']
    search_fields = ['question']
    date_hierarchy = 'date_created'

admin.site.register(DatasetXml, DatasetXmlAdmin)