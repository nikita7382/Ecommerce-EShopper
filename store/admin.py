from django.contrib import admin
from .models import Customer,OrderPlaced,Cart,Product

admin.site.register(Customer)
admin.site.register(OrderPlaced)
admin.site.register(Cart)
admin.site.register(Product)

# Register your models here.
