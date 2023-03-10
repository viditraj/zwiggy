from django.db import models
from vendor.models import Vendor
# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True) #URL of the category
    description = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = ("vendor", "category_name")

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name

RATINGS = [
    (1, ('1')),
    (2, ('2')),
    (3, ('3')),
    (4, ('4')),
    (5, ('5')),
]

class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    rating = models.IntegerField(choices=RATINGS, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_non_veg = models.BooleanField(null=True, blank=True)


    class Meta:
        unique_together = ("vendor", "food_title")

    def __str__(self):
        return self.food_title

