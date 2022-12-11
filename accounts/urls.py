# pages/urls.py
from django.urls import path
from .views import HomePageView, HitCreateView, HitListView, HitmanDetailView, HitmanListView, \
    HitUpdateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("hits/create/", HitCreateView.as_view(), name="create_hit"),
    path('hits/list/', HitListView.as_view(), name='list_hit'),
    path('hits/detail/<int:pk>', HitUpdateView.as_view(), name='update_hit'),
    path('hitmen/', HitmanListView.as_view(), name='list_hitman'),
    path('hitman/detail/<uuid:id>', HitmanDetailView.as_view(), name='detail_hitman'),
]
