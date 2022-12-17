from django.contrib import admin
from .models import Blog
from .forms import BlogForm

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','slug','created_by','created_date']
    ordering = ['-created_date']
    # form = BlogForm
    # fields = ['title','slug','short_content','long_content','created_by','created_date']
