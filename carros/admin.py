from django.contrib import admin
from .models import Garagem, CarroSalvo

@admin.register(Garagem)
class GaragemAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

@admin.register(CarroSalvo)
class CarroSalvoAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "ano", "preco", "garagem")
    search_fields = ("marca", "modelo")
    list_filter = ("marca", "ano", "garagem")
