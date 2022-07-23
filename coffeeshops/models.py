from django.db import models


class CafeOwner(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, default="")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self) -> str:
        return self.full_name


class CoffeeShopAddress(models.Model):
    line1 = models.CharField(max_length=40, default="")
    line2 = models.CharField(max_length=40, default="")
    city = models.CharField(max_length=20, default="")

    def __str__(self) -> str:
        try:
            return f"{self.coffee_shop.name} - {self.city}"
        except CoffeeShop.DoesNotExist:
            return str(self.city)


class CoffeeShop(models.Model):
    name = models.CharField(max_length=40)
    location = models.OneToOneField(
        CoffeeShopAddress,
        on_delete=models.SET_NULL,
        related_name="coffee_shop",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        CafeOwner,
        on_delete=models.CASCADE,
        related_name="coffee_shops",
    )
    slug = models.SlugField(editable=False, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Drink(models.Model):
    name = models.CharField(max_length=40)
    coffee_shop = models.ForeignKey(
        CoffeeShop,
        on_delete=models.CASCADE,
        related_name="drinks",
    )
    price = models.DecimalField(max_digits=7, decimal_places=3)
    stock_count = models.PositiveIntegerField()
    is_out_of_stock = models.BooleanField(editable=False)

    def __str__(self) -> str:
        return str(self.name)
