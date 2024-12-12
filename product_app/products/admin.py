from django.contrib import admin
from .models import Product, Invoice, Transaction

admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Transaction)
