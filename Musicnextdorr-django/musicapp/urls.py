from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name = 'home' ),
    path('post/<int:pk>', views.single_post, name = 'single_post'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name = 'register')
]