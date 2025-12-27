"""
URL configuration for project30 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from app.views import update_selection



urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu_view/',menu_view,name='menu_view'),
    path('menu/<str:category>/',menu_category, name='menu_category'),
    path('create_dish/',create_dish,name='create_dish'),
    path('create_review/',create_review, name='create_review'),
    # path('select/<int:dish_id>/',select_dish,name='select_dish'),
    path('menu/update-selection/', update_selection, name='update_selection'),






] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
