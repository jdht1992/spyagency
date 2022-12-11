# pages/urls.py
from django.urls import path
from .views import HomePageView, HitCreateView, HitListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("hit/create/", HitCreateView.as_view(), name="create_hit"),
    path('hit/list/', HitListView.as_view(), name='list_hit'),
]
