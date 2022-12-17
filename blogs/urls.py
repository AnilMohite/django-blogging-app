from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('blogs', blogs, name='blogs'),
    path('blog/<str:slug>', blog, name='blog'),
    path('about', about, name='about'),
    path('contact', contact, name='contact')
]
