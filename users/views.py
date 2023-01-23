from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blogs.models import Blog

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
            return redirect('login')
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
            return redirect('login')
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
    blogObj = Blog.objects.order_by('-created_date').all()
    if request.user.is_superuser:
        blogs = blogObj
    else:
        blogs = blogObj.filter(user_id=request.user)
    return render(request,'my-blogs.html',context={"blogs":blogs})
        