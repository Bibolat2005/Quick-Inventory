from django.contrib import admin
from .models import Category, Product, Transaction, CustomUser

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(CustomUser)