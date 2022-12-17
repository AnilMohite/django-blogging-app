from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Blog

class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    slug = forms.SlugField(max_length=150)
    img = forms.ImageField()
    short_content = forms.CharField(max_length=200, widget=AdminPagedownWidget())
    long_content = forms.CharField(widget=AdminPagedownWidget())
    created_by = forms.CharField(max_length=50)
    created_date = forms.DateTimeField()

    class Meta:
        model = Blog
        fields = "__all__"