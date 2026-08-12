"""
URL configuration for hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static
from django.shortcuts import render


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  
]


def error_400(request, exception=None):
    return render(request, "core/errors/400.html", status=400)


def error_403(request, exception=None):
    return render(request, "core/errors/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "core/errors/404.html", status=404)


def error_500(request):
    return render(request, "core/errors/500.html", status=500)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)