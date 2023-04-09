from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def doctor_dashboard(request):
    return render(request,'doctor/doctor_dashboard.html')

@login_required(login_url='/login')
def doctor_profile(request):
    if request.method == 'POST':
        curruser = request.user.username
        data = User.objects.get(user_id=curruser)
        return render(request, 'doctor/doctor_profile_update.html', context={"userprofile": data})
    curruser = request.user.username
    data = User.objects.get(username=curruser)
    return render(request, 'doctor/doctor_profile.html', context={"basicdata": data})