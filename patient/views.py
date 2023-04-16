from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

from doctor.models import Post,Category,Comment
from django.core.paginator import Paginator
import pytz
from datetime import datetime, timedelta
##for Google Calender API
from apiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

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

##Blogs
@login_required(login_url='/login')
def patient_blogs(request):
    posts = Post.objects.filter(is_published="1").order_by('-posted_at')
    categories = Category.objects.all()
    posts = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = posts.get_page(page)

    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request,'patient/patient_blogs.html',context)

@login_required(login_url='/login')
def patient_post(request,title):
    post = Post.objects.get(title=title)
    category = post.category
    related_posts = Post.objects.filter(category=category,is_published="1")
   
    recent_posts = Post.objects.filter(is_published="1").order_by('posted_at')
    
    categories = Category.objects.all()
    comments = Comment.objects.filter(post=post)
    
    # print(10*'--',posts)
    context = {
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'post':post,
        'categories': categories,
        'comments': comments,
    }
    return render(request,'patient/patient_post.html',context)

@login_required(login_url='/login')
def patient_search_view(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        #print(10*'---',keyword)

        posts = Post.objects.filter(title__icontains=keyword,is_published="1")
        categories = Category.objects.all()
        posts = Paginator(posts, 5)
        page = request.GET.get('page')
        posts = posts.get_page(page)

        context = {
            'posts': posts,
            'categories': categories,
            'searching':1,
            'keyword':keyword,
            }

    return render(request,'patient/patient_blogs.html',context)

@login_required(login_url='/login')
def patient_post_comment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        website = request.POST.get('website')
        post_id = request.POST.get('id')

        # print(10*'---',comment,post_id,name)
        post = Post.objects.get(id=post_id)

        c = Comment(name=name, email=email,comment=comment,website=website,post=post)
        c.save()
        return redirect('patient_post',title=post.title)

    return redirect('patient_blogs')

def patient_get_category(request,cat):
    category = Category.objects.get(name=cat)
    posts = Post.objects.filter(category=category,is_published="1")
    categories = Category.objects.all()
    # print(categories)
    posts = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = posts.get_page(page)
    

    context = {
        'posts': posts,
        'categories': categories,
        }

    return render(request,'patient/patient_blogs.html',context)

def patient_my_appointments(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds=Credentials.from_authorized_user_file('token.json',SCOPES)
    service = build("calendar", "v3", credentials=creds)
    res=get_events_by_summary(service,str(request.user.username))
    dict_list = []
    for sublist in res:
        dictionary = {'doctor': sublist[0],
                      'patient': sublist[1],
                      'appointment': sublist[2],
                      'start_date': sublist[3],
                      'start_time': sublist[4],
                      'end_date': sublist[5],
                      'end_time': sublist[6]}
        dict_list.append(dictionary)
    context = {'appointments': dict_list}
    return render(request,'patient/patient_myappointments.html',context)


def patient_book_appointment(request):
    tot_doctors = User.objects.filter(user_status="Doctor")
    return render(request,'patient/patient_book_appointment.html',context={"tot_doctors": tot_doctors})


def patient_confirmbook(request,docname):
    if(request.method=='POST'):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        fdate = request.POST.get('fdate')
        ftime = request.POST.get('ftime')
        frequired = request.POST.get('frequired')
        fmessage = request.POST.get('fmessage')
        doctorname = request.POST.get('doctorname')
        timezone = pytz.timezone('Asia/Kolkata')
        start_time = timezone.localize(datetime(int(str(fdate)[0:4]), int(str(fdate)[5:7]), int(str(fdate)[8::]), int(str(ftime)[0:2]),int(str(ftime)[3::]) , 0))
        end_time = start_time + timedelta(minutes=45)
        #-----service creation
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds=Credentials.from_authorized_user_file('token.json',SCOPES)
        service = build("calendar", "v3", credentials=creds)
        ##----calender id and events checking
        result=checking_calender_ids(service,doctorname,start_time,end_time)
        if(result[1]==1):
            userrr=User.objects.get(username=request.user.username)
            return render(request,'patient/patient_confirmbook.html',context={'doctorname':doctorname,'userdetails':userrr,"eventnotconfirm":1})
        else:
            description="Appointment for "+frequired
            forperson=str(fname)+"  "+str(lname)
            l=create_event(service,start_time,end_time,str(request.user.username), description=description, location=forperson,cid=result[0])
            #########################################
            ############For Form ####################
            start = str(start_time)
            dt = datetime.fromisoformat(start)
            start=str(dt.strftime('%d'))+" "+str(dt.strftime('%b'))+" "+str(dt.strftime('%Y'))
            start_time=dt.strftime('%I:%M %p')
            # Convert the endttime object to a string in AM/PM format
            end = str(end_time)
            dt = datetime.fromisoformat(end)
            end=start=str(dt.strftime('%d'))+" "+str(dt.strftime('%b'))+" "+str(dt.strftime('%Y'))
            end_time=dt.strftime('%I:%M %p')
            sublist=[doctorname,str(request.user.username),fname+" "+lname,description,start,start_time,end,end_time]
            dictionary = {'doctor': sublist[0],
                      'patient': sublist[1],
                      'pfnln':sublist[2],
                      'appointment': sublist[3],
                      'start_date': sublist[4],
                      'start_time': sublist[5],
                      'end_date': sublist[6],
                      'end_time': sublist[7]}

            return render(request,'patient/sample_printout.html',context={'appointments': dictionary})
        #print("\nStart time :",start_time)
        #print("\n"*5,"DEtails\n"+"first name : "+str(fname)+"\n"+"last name : "+str(lname)+"\n"+"Date  : "+str(fdate)+"\n"+"Time : "+str(ftime)+"\n"+"Required Speciality : "+str(frequired)+"\n"+"Message : "+str(fmessage))

        
    #print(" \n\n\ndoctor name "+docname+"\n Patient_name : "+request.user.username+"\n\n")
    userrr=User.objects.get(username=request.user.username)
    return render(request,'patient/patient_confirmbook.html',context={'doctorname':docname,'userdetails':userrr})



####Utility Function for calender id and events
def checking_calender_ids(service,dname,sttime,endtime): 
        calendar_list = service.calendarList().list().execute()
        endtime = endtime + timedelta(minutes=1)
        calendar_id=""
        for calendar in calendar_list['items']:
            if calendar['summary'] ==dname:
                calendar_id = calendar['id']
                break
        ##Find Whether the Events are in between there or not
        page_token = None
        l=[]
        while True:
            events = service.events().list(calendarId=calendar_id, timeMin=sttime.isoformat(), timeMax=endtime.isoformat(), singleEvents=True, orderBy='startTime').execute()
            for event in events['items']:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    start_time = datetime.fromisoformat(start)
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    end_time = datetime.fromisoformat(end)
                    l.append('Event:'+event["summary"])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        print(l)
        if(len(l)==0):
            return [str(calendar_id),0]
        else:
            return [calendar_id,1]
        
###for event creation
def create_event(service,start_time,end_time, summary, description=None, location=None,cid=None):  
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId=cid, body=event).execute()

##For getting appointments for particular user
def get_events_by_summary(service,summary):
    calendar_list = service.calendarList().list().execute()
    l=[]
    # Loop through each calendar and fetch the events that match the specified summary
    for calendar in calendar_list['items']:
        now = datetime.now(pytz.timezone('Asia/Kolkata'))
        time_max = now + timedelta(days=7)
        start_time = now.astimezone(pytz.utc).isoformat()
        end_time = time_max.astimezone(pytz.utc).isoformat()
        calendar_id = calendar['id']
        calendar_summary = calendar['summary']
        #print(f'Checking calendar "{calendar_summary}"...')
        #print(calendar_id)
        try:
            events_result = service.events().list(calendarId=calendar_id, timeMin=start_time, timeMax=end_time, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not events:
                new=[]
                #print(f'No events found in the "{calendar_summary}" calendar for the next week.')
            else:
                for event in events:
                    if event.get('summary') == summary:
                        new=[]
                        # Convert the starttime object to a string in AM/PM format
                        start = event['start']['dateTime']
                        dt = datetime.fromisoformat(start)
                        start=str(dt.strftime('%d'))+" "+str(dt.strftime('%b'))+" "+str(dt.strftime('%Y'))
                        start_time=dt.strftime('%I:%M %p')
                        # Convert the endttime object to a string in AM/PM format
                        end = event['end']['dateTime']
                        dt = datetime.fromisoformat(end)
                        end=start=str(dt.strftime('%d'))+" "+str(dt.strftime('%b'))+" "+str(dt.strftime('%Y'))
                        end_time=dt.strftime('%I:%M %p')
                        new.append(str(calendar['summary']))
                        new.append(event['location'])
                        new.append(event['description'])
                        new.append(start)
                        new.append(start_time)
                        new.append(end)
                        new.append(end_time)
                        l.append(new)
        except Exception as e:
            print("hello" ,e)
            pass
    #print(l)
    return l
