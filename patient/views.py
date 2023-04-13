from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

from doctor.models import Post,Category,Comment
from django.core.paginator import Paginator


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

