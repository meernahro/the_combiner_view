"""
URL configuration for the_combiner_view project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import DashboardView, get_exchanges, get_channels
from latest_tokens.urls import urlpatterns as latest_tokens_urls


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('get-exchanges/', get_exchanges, name='get_exchanges'),
    path('get-channels/', get_channels, name='get_channels'),
    path('admin/', admin.site.urls),
    path('trading/', include('trading.urls', namespace='trading')),
]

urlpatterns += latest_tokens_urls

# Add this for serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
