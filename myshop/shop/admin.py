from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    # Поле slug устанавливается авт. с пом. поля name:
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    # Поля, которые можно редактировать (они должны быть в list_display):
    list_editable = ['price', 'available']
    # Поле slug устанавливается авт. с пом. поля name:
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}