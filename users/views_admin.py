from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blogs.models import Blog,Contact
from django.contrib.auth.models import User
from django.conf import settings
import datetime

def adminPanel(request):
    context = {}
    context['ttl_pending_review_count'] = Blog.objects.filter(is_ready_for_review=True).count()
    context['ttl_contact_us_count'] = Contact.objects.count()
    context['ttl_user_count'] = User.objects.count()

    return render(request,'admin-panel.html',context=context)


def reviewBlog(request):
    context = {}
    context['pending_blogs'] = Blog.objects.filter(is_ready_for_review=True,is_approved=False)
    return render(request,'admin-review-blog.html',context=context)


def userManage(request):
    context = {}
    context['users'] = User.objects.all()
    # print(context['users'][1].__dict__)
    return render(request,'admin-users.html',context=context)


def publishBlog(request,pk):
    blogForApproval = Blog.objects.get(id = pk)
    blogForApproval.is_approved = True
    blogForApproval.is_ready_for_review = False
    blogForApproval.save()
    messages.success(request, 'Blog Published Successfully!')
    
    return redirect('/admin-view/review-blog/')


def contactUS(request):
    context = {}
    context['contacts'] = Contact.objects.all()
    return render(request,'admin-contact-us.html',context=context)