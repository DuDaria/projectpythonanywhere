"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import static
from blogproject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('advito/', include('advito.urls'))
]

# STATIC_URLS
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# MEDIA_URLS
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# STATIC_URL - путь статичных файлов
# STATIC_ROOT - в какой папке находятся статичные файлы
# Функцией static регистрирует все пути