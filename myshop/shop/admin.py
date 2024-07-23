from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # Поле slug устанавливается авт. с пом. поля name:
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    # Поля, которые можно редактировать (они должны быть в list_display):
    list_editable = ['price', 'available']
    # Поле slug устанавливается авт. с пом. поля name:
    prepopulated_fields = {'slug': ('name',)}