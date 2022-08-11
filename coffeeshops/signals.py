from pickle import FALSE
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .models import CafeOwner ,CoffeeShop
from utils import create_slug


@receiver(post_save,sender=CafeOwner)
def send_new_owner_email(sender,instance,created,**kwargs):
    print("called")
    if created == True:
        print("true")
        send_mail(
    'New Cafe Owner',
    'A new cafe owner has joined named <FULL_NAME_OF_CAFE_OWNER>.',
    'sender@test.com',
    ["receiver@test.com"],   
    )   
    print("end")

@receiver(pre_save,sender=CoffeeShop)
def slugify_coffee_shop(instance,sender,**kwargs):
    if not instance.slug:
       instance.slug = create_slug(instance)
       
