from django.contrib import admin
from .models import Categoria, Requisito, Servicio


class ServicioInline(admin.TabularInline):
    model = Servicio
    extra = 0


class RequisitoInline(admin.TabularInline):
    model = Requisito
    extra = 0


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    inlines = (ServicioInline,)


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'dias_habiles', 'costo')
    search_fields = ('nombre', 'categoria__nombre', 'descripcion')
    list_filter = ('categoria',)
    inlines = (RequisitoInline,)


class RequisitoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'servicio')
    search_fields = ('descripcion', 'servicio__nombre')
    list_filter = ('servicio',)


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Requisito, RequisitoAdmin)