from django.contrib import admin
from .models import *

# Register your models here.



admin.site.site_header = "DGRE"
admin.site.site_title = "DGRE "
admin.site.index_title = "DGRE"



class pointer(admin.ModelAdmin):
    list_display = ["title", "longitude", "latitude", "create_at"]

admin.site.register(Pointers, pointer)
admin.site.register(GeoFile)



