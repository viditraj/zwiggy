from django.db import models
from django.db import models
from accounts.models import User
from vendor.models import Vendor
# Create your models here.

RATINGS = [
    (1, ('1')),
    (2, ('2')),
    (3, ('3')),
    (4, ('4')),
    (5, ('5')),
]

class VendorReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=True, null=True)
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating_given = models.IntegerField(choices=RATINGS, null=True, blank=True)
    def __str__(self):
        return self.content