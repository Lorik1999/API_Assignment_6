"""API URL Configuration

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
from django.urls import path
from API_server import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home', views.home),
    # re_path(r'^pizza/(?P<pizza_id>)/$', views.Get_Pizza.get,name='Get_Pizza'),
    # re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    path('pizza/',views.get_pizza),
    path('pizza/<int:pizza_id>/',views.get_pizza),
    path('order',views.order_pizza),
    path('order/<slug:order_id>/',views.order_pizza),
    path('order/deliverytime/<int:order_id>/', views.get_delivery_time),
    path('order/cancel/<int:order_id>', views.cancel_order),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)