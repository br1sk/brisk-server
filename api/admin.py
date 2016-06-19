from django.contrib import admin
from models import *


class Admin(admin.ModelAdmin):
    pass


admin.site.register(Product, Admin)
admin.site.register(Classification, Admin)
admin.site.register(Reproducibility, Admin)
admin.site.register(Area, Admin)
admin.site.register(Authorization, Admin)
