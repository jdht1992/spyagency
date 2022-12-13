# pages/urls.py
from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (HitCreateView, HitListView, HitmanDetailView, HitmanListView,
                    HitUpdateView, SignupPageView, post_hitlbul)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', SignupPageView.as_view(), name='signup'),
    path("hits/create/", HitCreateView.as_view(), name="create_hit"),
    path('hits/', HitListView.as_view(), name='list_hit'),
    path('hits/detail/<int:pk>', HitUpdateView.as_view(), name='update_hit'),
    path('hits/bulk/', post_hitlbul, name='update_hit_bulk'),
    path('hitmen/', HitmanListView.as_view(), name='list_hitman'),
    path('hitmen/detail/<uuid:id>', HitmanDetailView.as_view(), name='detail_hitman'),
]
