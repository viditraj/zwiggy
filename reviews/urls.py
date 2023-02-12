from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.reviews, name='reviews'),
   # path('increment_likes/<int:review_id>/', views.increment_likes, name='increment_likes'),
]