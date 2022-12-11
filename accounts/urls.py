# pages/urls.py
from django.urls import path
from .views import HomePageView, HitCreateView, HitListView, HitDetailView, HitmanDetailView, HitmanListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("hit/create/", HitCreateView.as_view(), name="create_hit"),
    path('hit/list/', HitListView.as_view(), name='list_hit'),
    path('hit/detail/<int:pk>', HitDetailView.as_view(), name='detail_hit'),
    path('hitman/list/', HitmanListView.as_view(), name='list_hit'),
    path('hitman/detail/<uuid:id>', HitmanDetailView.as_view(), name='detail_hitman'),
]
