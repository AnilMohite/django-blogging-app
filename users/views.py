from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blogs.models import Blog
import os
from django.conf import settings
import datetime

# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')          
        else:
            messages.warning(request,'Invalid Username or Password')  
            return redirect('/user/login/')
    else:
        form = AuthenticationForm()
        return render(request ,'login.html',context={'form':form})    

def registerUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request,'Confirm password does not match!')
            # return render(request ,'register.html',context={"form":form})
            return redirect('register')
        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            messages.success(request,'User registered successfully! Login Here!')
            return redirect('/user/login/')
    else:
        form = AuthenticationForm()
        return render(request ,'register.html',context={"form":form})

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def forgotPassword(request):
    if request.method == 'POST':
        return render(request, 'forgot_password.html',context={})
    else:
        return render(request, 'forgot_password.html',context={})

@login_required(login_url='login')
def myProfile(request):
    user = User.objects.get(username = request.user)
    if request.method == 'POST':
        if request.POST['form_type'] == 'profile_update':
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            messages.success(request,"Profile updated successfully!")

        elif request.POST['form_type'] == 'password_update':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            if new_password != confirm_new_password:
                messages.warning(request,'Confirm password does not match!')
            else:
                old_password_check = request.user.check_password(old_password)
                if old_password_check:
                    user = User.objects.get(username=request.user)
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request,user)
                    messages.success(request,'Password Changed Successfully!')
                else:
                    messages.warning(request,'Incorrect password, please try again!')

    return render(request, 'my-profile.html', context={"user":user})

@login_required(login_url='login')
def myBlogs(request):
    context ={}
    try:
        blog_objs = Blog.objects.filter(user_id = request.user)
        context['approved_blogs'] = blog_objs.filter(is_approved = True)
        context['not_sent_for_approval'] = blog_objs.filter(is_ready_for_review = False).filter(is_approved = False)
        context['pending_review'] = blog_objs.filter(is_ready_for_review = True).filter(is_approved = False)
        # context['blogs_obj'] = blog_objs

    except Exception as e:
        print(e)
    print(context)
    return render(request,'my-blogs.html',context=context)
        
@login_required(login_url='login')
def deleteBlog(request,pk):
    blogObj = Blog.objects.get(id=pk)
    try:
        if blogObj.user_id == request.user or request.user.is_superuser:
            if blogObj.img.name:
                imgPath = os.path.join(settings.MEDIA_ROOT,blogObj.img.name)
                os.remove(imgPath)
            blogObj.delete()
            messages.success(request, 'Blog deleted successfully!')
        else:
            messages.success(request, 'Unauthorized!')
    except Exception as e:
        print(e)

    return redirect('/user/my-blogs/')

@login_required(login_url='login')
def addBlog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        short_content = request.POST.get('short_content')
        long_content = request.POST.get('long_content')
        blog_image = request.FILES.get('blog_image')
        user = request.user
        
        Blog.objects.create(title=title,short_content=short_content,long_content=long_content,img=blog_image,created_by=request.user,user_id=user,created_date=datetime.datetime.now())
        messages.success(request,'Blog save successfully!')
        return redirect('/user/my-blogs/')
    return render(request,'add-blog.html',context={})

def updateBlog(request,pk):
    context = {}
    blogObj = Blog.objects.get(id=pk)
    if request.method == 'POST':
        if (request.user==blogObj.user_id) or (request.user.is_superuser):
            
            blogObj.title = request.POST.get('title')
            blogObj.short_content = request.POST.get('short_content')
            blogObj.long_content = request.POST.get('long_content')
            blog_image = request.FILES.get('blog_image')

            old_img = blogObj.img.name
            if not blog_image is None:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_img))
                    blogObj.img = blog_image
                except:
                    messages.warning(request, f"Unable to update blog picture!")

            blogObj.is_approved = False
            blogObj.created_by = request.user.username
            blogObj.created_date = datetime.datetime.now()
            blogObj.save()
            messages.success(request,'Blog updated successfully!')
            return redirect('/user/my-blogs/')
        else:
            return redirect('/')
    else:
        context['blog_obj'] = blogObj
    return render(request,'update-blog.html',context=context)

def sendForReview(request,pk):
    print('asf',pk)
    blogForReview = Blog.objects.get(id=pk)
    if blogForReview.is_ready_for_review == False:
        blogForReview.is_ready_for_review = True
        messages.success(request, 'Blog Sent for a Review!')
    else:
        blogForReview.is_ready_for_review = False
        messages.success(request, 'Blog Withdrawn form a Review!')
    blogForReview.save()

    return redirect('/user/my-blogs/')
    