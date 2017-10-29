from django.contrib import admin

# Register your models here.

from .model import Item

admin.site.register(Item)
#registers model with item
