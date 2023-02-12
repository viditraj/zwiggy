from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

# @receiver(post_save, sender=User)
# def post_save_create_user_profile(sender, instance, created, **kargs):
#     if created:
#         # new profile 
#        UserProfile.objects.create(user=instance)
#     else:
#         # update exisitng profile
#         try:
#            profile = UserProfile.objects.get(user=instance)
#            profile.save()
#         except:
#             # if the profile does not exist but the user exits then create the profile for that user. 
#               UserProfile.objects.create(user=instance)



