from django.apps import AppConfig


class CoffeeshopsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "coffeeshops"

    def ready(self) -> None:
        import coffeeshops.signals