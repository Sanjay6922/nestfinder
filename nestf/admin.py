from django.contrib import admin
from .import models
from .models import Reg_form, Reviews
# Register your models here.
admin.site.register(Reg_form)
admin.site.register(Reviews)   
# admin.site.register(models.Product)
# admin.site.register(models.ProductImage)   


