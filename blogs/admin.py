from django.contrib import admin
from .models import Blog, Contact

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','slug','created_by','created_date']
    ordering = ['-created_date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user)
        
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','message']
    ordering = ['-created_date']