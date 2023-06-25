from django.urls import path
from . import views 
urlpatterns = [
    path('', views.kbItems, name = 'kbItems'),
    path('new/',views.addKBItem, name = 'addKBItem'),
    path('search/', views.queryItems, name = 'queryItems')
]