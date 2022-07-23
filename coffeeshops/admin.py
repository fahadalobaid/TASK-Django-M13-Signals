from django.contrib import admin

from coffeeshops import models


@admin.register(models.CafeOwner)
class CafeOwnerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CoffeeShopAddress)
class CoffeeShopAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CoffeeShop)
class CoffeeShopAdmin(admin.ModelAdmin):
    readonly_fields = ("slug",)


@admin.register(models.Drink)
class DrinkAdmin(admin.ModelAdmin):
    readonly_fields = ("is_out_of_stock",)
