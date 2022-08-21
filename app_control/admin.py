from django.contrib import admin
from app_control.models import InventoryGroup, InventoryItem, Shop, InvoiceItem, Invoice

admin.site.register(( 
    InventoryItem, InventoryGroup, Shop, Invoice, InvoiceItem
))
