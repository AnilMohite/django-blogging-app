from django.urls import path, include
from .views_admin import *

urlpatterns = [
    path('admin-panel/', adminPanel, name='admin-panel'),
    path('review-blog/', reviewBlog, name='review-blog'),
    path('user-manage/', userManage, name='user-manage'),

    path('publish-blog/<int:pk>', publishBlog, name='publish-blog'),
]
