from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginUser, name='login'),
    path('register/', registerUser, name='register'),
    path('logout/', logoutUser, name='logout'),
    path('forgot-password/', forgotPassword, name='forgot-password'),
    path('my-profile/', myProfile, name='my-profile'),
    path('my-blogs/', myBlogs, name='my-blogs'),
    path('delete-blog/<id>', deleteBlog, name='delete-blog'),
]
