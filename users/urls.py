from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', loginUser, name='login'),
    path('register/', registerUser, name='register'),
    path('logout/', logoutUser, name='logout'),
    path('forgot-password/', forgotPassword, name='forgot-password'),

    path('my-profile/', myProfile, name='my-profile'),
    path('my-blogs/', myBlogs, name='my-blogs'),
    path('delete-blog/<int:pk>', deleteBlog, name='delete-blog'),
    path('add-blog', addBlog, name='add-blog'),
    path('update-blog/<int:pk>', updateBlog, name='update-blog'),
    path('send-for-review/<int:pk>', sendForReview, name="send-for-review"),

    path('admin-view/', include('users.urls_admin')),
]
