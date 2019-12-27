from django.contrib import admin
from .models import Acid, Hydroxide, Container


# Register your models here.
class AcidAdmin(admin.ModelAdmin):
    list_display = ['name', 'mol_H', 'all_mol']
    list_filter = ['mol_H']


class HydroxideAdmin(admin.ModelAdmin):
    list_display = ['name', 'mol_OH', 'all_mol']
    list_filter = ['mol_OH']


class ContainerAdmin(admin.ModelAdmin):
    list_display = ['pH', 'V', ]


admin.site.register(Acid, AcidAdmin)
admin.site.register(Hydroxide, HydroxideAdmin)
admin.site.register(Container, ContainerAdmin)