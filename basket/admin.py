from django.contrib import admin
from basket.models import Basket


class BasketAdmin( admin.ModelAdmin):
    list_display = (
        "basket_id",
        "user_id",
        "product_id",
        "product_name",
        "quantity",
        )
admin.site.register(Basket, BasketAdmin)




