from django import forms
from .models import VendorReviews

class ReviewForm(forms.ModelForm):
    class Meta:
        model = VendorReviews
        fields = ['content', 'rating_given',]