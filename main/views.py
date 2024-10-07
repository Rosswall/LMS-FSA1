from django.shortcuts import render,redirect
from django.contrib import messages
from module_group.models import ModuleGroup, Module
from user.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from user.forms import UserForm
from django.contrib.auth.hashers import make_password


def loginPage(request):
    page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('main:home')
        else:
            messages.error(request, "Invalid username or password")
    context = {'page': page}
    return render(request,'login_register.html',context)

# def loginPage(request):
#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect('main:home')
    
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         try:
#             user = User.objects.get(username=username)
#             if check_password(password, user.password):  # Check hashed password
#                 login(request, user)
#                 return redirect('main:home')
#             else:
#                 messages.error(request, "Invalid username or password")
#         except User.DoesNotExist:
#             messages.error(request, "User does not exist")

#     context = {'page': page}
#     return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('main:home')

def registerPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('main:register')

        user = User.objects.create(
            username=username,
            password=make_password(password),  
            email=email,
        )
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('main:login')  # Redirect to the login page after successful registration
            
    return render(request,'login_register.html')
@login_required(login_url='login/')
def home(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'home.html', {
        'module_groups': module_groups,
        'modules': modules,
    })

def base_view(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'base.html', {
        'module_groups': module_groups,
        'modules': modules,
    })


