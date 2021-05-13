"""shopcard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from .import shop
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",shop.home,name='home'),
    path("Contact/",shop.Contact,name='contact'),
    path("About/",shop.About,name='about'),
    path("Tracker/",shop.Tracker,name='tracker'),
    path("Search/",shop.Search,name='search'),
    path("Productview/<int:myid>",shop.Productview,name='prodview'),
    path("Checkout/",shop.Checkout,name='checkout'),
    path("Handlerequest/",shop.Handlerequest,name="handlerquest")

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
