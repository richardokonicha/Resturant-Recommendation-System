from django.contrib import admin
from .models import Restaurant, Dish


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    fields = ("name", "address", "image_url", ("longitude", "latitude"))
    list_display = ("name", "address", "rating")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "rating")
    list_filter = ("price", "rating")
    raw_id_fields = ("restaurant",)
