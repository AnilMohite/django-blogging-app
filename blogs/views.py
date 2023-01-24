from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    blogs = Blog.objects.all().order_by('-created_date')[:3]
    return render(request,'index.html',context={'blogs':blogs})

def blogs(request):
    blogs = Blog.objects.all().order_by('-created_date')
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'blogs.html',context={'blogs':blogs,'page_obj': page_obj})

def blog(request,slug):
    blog = Blog.objects.filter(slug=slug).first()
    return render(request,'blog_view.html',context={'blog':blog})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        cus = Contact(name=name,email=email,message=message,created_date=datetime.datetime.now())
        cus.save()
        messages.success(request, 'Thank you for visiting our website and we look forward to connecting with you!')
    return render(request,'contact_us.html')
