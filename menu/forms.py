from django import forms

from accounts.validators import allow_only_images_validator
from .models import Category, FoodItem
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_images_validator])
    
    class Meta:
        model = FoodItem
        fields = ['food_title', 'category', 'description', 'is_available', 'is_non_veg', 'price', 'image']