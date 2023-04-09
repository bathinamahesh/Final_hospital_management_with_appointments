from django.shortcuts import render
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required




User = get_user_model()
# Create your views here.


@login_required(login_url='/login')
def patient_dashboard(request):
    return render(request,'patient/patient_dashboard.html')


@login_required(login_url='/login')
def patient_profile(request):
    '''if request.method == 'POST':
        curruser = request.user.username
        data = User.objects.get(user_id=curruser)
        return render(request, 'patient/patient_profile.html', context={"userprofile": data})'''
    curruser = request.user.username
    data = User.objects.get(username=curruser)
    return render(request, 'patient/patient_profile.html', context={"basicdata": data})