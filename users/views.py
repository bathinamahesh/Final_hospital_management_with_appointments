from django.shortcuts import render

# Create your views here.
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()


def register(request):
    if request.method == 'POST':
        user_status=request.POST.get('user_config')
        first_name = request.POST.get('user_firstname')
        last_name = request.POST.get('user_lastname')
        profile_pic=""
        if "profile_pic" in request.FILES:
            profile_pic = request.FILES['profile_pic']
            #print("__"*20,"mahesh")
        #User_name
        username = request.POST.get('user_id')
        email = request.POST.get('email')
        sex = request.POST.get('user_sex')
        password = request.POST.get('password')
        confirm_password=request.POST.get('conf_password')
        address = request.POST.get('add')
        address+=" , "
        address+=request.POST.get('city')
        address+=" , "
        address+=request.POST.get('state')
        address+=" , "
        address+=request.POST.get('pincode')
        variable = User.objects.filter(username=username)
        if(len(list(variable)) == 0 and str(password)==str(confirm_password)):
            user = User.objects.create_user(user_status=user_status,first_name=first_name,last_name=last_name,profile_pic = profile_pic,username = username,
                    email=email,
                    sex=sex,
                    password=password,
                    confirm_password=confirm_password,
                    address =address,
                )
            user.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', context={
                'errorcame': 1,
            })
    return render(request, 'users/register.html', context={'errorcame': 0})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            obj = User.objects.get(username=username)
            if obj.user_status == "Doctor":
                return redirect('doctor_dashboard')
            elif(obj.user_status == "Patient"):
                return redirect('patient_dashboard')
        else:
            return render(request, 'users/login.html', context={'errorlogin': 1})

    return render(request, 'users/login.html', context={'errorlogin': 0})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('login')
