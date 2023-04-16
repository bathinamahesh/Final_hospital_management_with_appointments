from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from .models import Post,Category,Comment
from django.core.paginator import Paginator
import pytz
from datetime import datetime, timedelta
##for Google Calender API
from apiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

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
    

##Blogs
@login_required(login_url='/login')
def doctor_blogs(request):
    posts = Post.objects.filter(is_published="1").order_by('-posted_at')
    categories = Category.objects.all()
    posts = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = posts.get_page(page)

    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request,'doctor/doctor_blogs.html',context)

@login_required(login_url='/login')
def post(request,title):
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
    return render(request,'doctor/doctor_post.html',context)

@login_required(login_url='/login')
def search_view(request):
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

    return render(request,'doctor/doctor_blogs.html',context)

@login_required(login_url='/login')
def post_comment(request):
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
        return redirect('post',title=post.title)

    return redirect('doctor_blogs')

def get_category(request,cat):
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

    return render(request,'doctor/doctor_blogs.html',context)

def myblogs(request):
    posts = Post.objects.filter(is_published="1",user=str(request.user.username)).order_by('-posted_at')
    categories = Category.objects.all()
    posts = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = posts.get_page(page)

    context = {
        'posts': posts,
        'categories': categories,
    }

    return render(request,'doctor/doctor_blogs.html',context)

def upload_blog(request):
    upload_done = 0
    if request.method == 'POST':
        assign_author = request.user.username
        assign_title = request.POST.get('assign_title')
        assign_cat = request.POST.get('assign_class')
        tagss="#"+assign_cat
        assign_desc = request.POST.get('assign_desc')
        assign_summary = request.POST.get('assign_des')
        checkbox_value = request.POST.get('checking')
        if "assignupload" in request.FILES:
            #print("___"*20)
            upload = request.FILES['assignupload']
            """fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            print("__"*30, "__*********"*20, file_url)"""
        assign_cat=Category.objects.get(name=assign_cat)
        if checkbox_value:
            print("__"*20,"mahesh")
            c=Post(category=assign_cat,user=assign_author,title=assign_title,thumbnail=upload,description=assign_desc,summary=assign_summary,tags=tagss,is_published=0)
            upload_done = 2
        else:
            c=Post(category=assign_cat,user=assign_author,title=assign_title,thumbnail=upload,description=assign_desc,summary=assign_summary,tags=tagss)
            upload_done = 1
        c.save()
        
    user_name=request.user.username
    categories = Category.objects.all()
    return render(request, 'doctor/doctor_madepost.html', context={"upload_done": upload_done, "total_categories": categories,"user_name":user_name})

def doctor_drafts(request):
    posts = Post.objects.filter(is_published="0",user=str(request.user.username)).order_by('-posted_at')
    categories = Category.objects.all()
    posts = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = posts.get_page(page)

    context = {
        'posts': posts,
        'categories': categories,
    }
    if request.method == 'POST':
        post_id = request.POST.get('id')
        posts = Post.objects.filter(id=post_id)
        return render(request,"doctor/doctor_.html",context)



    return render(request,"doctor/doctor_drafts.html",context)

def modify(request,pid):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        title = request.POST.get('assign_title')
        category = request.POST.get('assign_class')
        category=Category.objects.get(name=category)
        description = request.POST.get('assign_desc')
        summary = request.POST.get('assign_des')
        if "assignupload" in request.FILES:
            upload = request.FILES['assignupload']
        post.title=title
        post.category=category
        post.description=description
        post.summary=summary
        post.is_published=1
        post.thumbnail=upload
        post.save()
        return redirect('doctor_drafts')
    posts=Post.objects.get(id=int(pid))
    print(" __"*20,posts)
    categories = Category.objects.all()
    context={
        "post":posts,
        'categories': categories
    }

    return render(request,"doctor/forsubmission.html",context)
def view_appointments(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds=Credentials.from_authorized_user_file('token.json',SCOPES)
    service = build("calendar", "v3", credentials=creds)
    result=get_aevents_by_summary(service,str(request.user.username))
    #print(result)
    dict_list=[]
    for sublist in result:
        dictionary = {'doctor': sublist[0],
                      'patient': sublist[1],
                      'appointment': sublist[2],
                      'start_date': sublist[3],
                      'start_time': sublist[4],
                      'end_date': sublist[5],
                      'end_time': sublist[6],
                    }
        dict_list.append(dictionary)
    context_dict = {'appointments': dict_list}
    return render(request,"doctor/viewappointments.html",context_dict)



def get_aevents_by_summary(service,dname):
    calendar_list = service.calendarList().list().execute()
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    #now=now+timedelta(hours=1,minutes=30)
    time_max = now + timedelta(days=7)
    start_time = now.astimezone(pytz.utc)
    end_time = time_max.astimezone(pytz.utc)
    l=[]
    ####Finding Calender ID
    calendar_id=""
    for calendar in calendar_list['items']:
        if calendar['summary'] ==dname:
                calendar_id = calendar['id']
                break
    # Loop through each calendar and fetch the events that match the specified summary
    try:
            events_result = service.events().list(calendarId=calendar_id, timeMin=start_time.isoformat(), timeMax=end_time.isoformat(), singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not events:
                pass
            else:
                for event in events:
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
    return l
