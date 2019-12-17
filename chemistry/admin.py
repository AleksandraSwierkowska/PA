from django.contrib import admin
from .models import Acid, Hydroxide


# Register your models here.
class AcidAdmin(admin.ModelAdmin):
    list_display = ['name', 'mol_H', 'all_mol']
    list_filter = ['mol_H']


class HydroxideAdmin(admin.ModelAdmin):
    list_display = ['name', 'mol_OH', 'all_mol']
    list_filter = ['mol_OH']


admin.site.register(Acid, AcidAdmin)
admin.site.register(Hydroxide, HydroxideAdmin)
