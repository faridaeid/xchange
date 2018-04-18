from django.contrib import admin

from .models import *

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(StoreCategories)
admin.site.register(Cart)
admin.site.register(CartProducts)
admin.site.register(Transaction)
