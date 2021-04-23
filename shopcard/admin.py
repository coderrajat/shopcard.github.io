from django.contrib import admin
from . models import product, contact, checkout, updateorder

admin.site.register(product)
admin.site.register(contact)
admin.site.register(checkout)
admin.site.register(updateorder)