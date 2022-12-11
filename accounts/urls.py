# pages/urls.py
from django.urls import path
from .views import HomePageView, HitCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("hit/create/", HitCreateView.as_view(), name="create_hit"),
]
