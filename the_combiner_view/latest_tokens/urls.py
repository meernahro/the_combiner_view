# the_combiner_view/latest_tokens/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_latest_tokens/', views.get_latest_tokens, name='get_latest_tokens'),
]