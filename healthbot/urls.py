from django.urls import path
from . import views

urlpatterns = [
    path('/index', views.index, name='index'),
    path('chat/', views.chat, name='chat'),
    path('', views.home, name='home'),
    path('medications/', views.page1, name='medications'),
    path('conditions/', views.page2, name='conditions'),
    path('other/', views.page3, name='other'),
]
