from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Animal)
admin.site.register(TempretureTest)
admin.site.register(TempretureResult)
admin.site.register(MilkTest)
admin.site.register(MilkResult)