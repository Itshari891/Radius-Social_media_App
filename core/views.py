from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . forms import SignupForm,SigninForm
from . models import Profile,Post,LikePost,FollowersCount
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.

@login_required(login_url="signin")
def index(request):
    login_user=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=login_user)
    posts=Post.objects.all()
    likes=LikePost.objects.all()
    

    #--------------------to show post of people followed by the loggedin user---------------------   
    user_following_list=[]
    feed=[]
    user_followings=FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_followings:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feeds=Post.objects.filter(user=usernames).order_by('created_date')
        feed.append(feeds)

    my_posts=Post.objects.filter(user=request.user.username).order_by('created_date')    
    feed.append(my_posts)
    feed_list= list(chain(*feed))
    #----------------------suggestion list-----------------------------------------
    all_users=User.objects.all()
    user_following_all=[]
    

    for user in user_followings:
        following=User.objects.get(username=user.user)
        user_following_all.append(following)
    
    new_suggestion_list=[x for x in list(all_users) if x not in list(user_following_all)]
    current_user=User.objects.filter(username=request.user.username)
    final_suggestion_list=[user for user in list(new_suggestion_list) if (user not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile=[]
    profile_list=[]

    for user in final_suggestion_list:
        username_profile.append(user.id)

    for id in username_profile:
        profiles=Profile.objects.filter(id_user=id)
        profile_list.append(profiles)
    
    suggestion_list=list(chain(*profile_list))
    print(list(all_users))
    print(user_following_all)
    print(new_suggestion_list)
    print(suggestion_list)
    return render(request, "index.html",context={'user_profile':user_profile,'posts':feed_list,"liked":likes,"login_user":login_user,"suggestions":suggestion_list[:4]})

@login_required(login_url="signin")    
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)

    if request.method == "POST":
        username=request.POST["username"]
        username_object=User.objects.filter(username__icontains=username)
        username_list=[]
        profile_list=[]

        for user in username_object:
            username_list.append(user.id)

        for id in username_list:
            profiles=Profile.objects.filter(id_user=id)
            profile_list.append(profiles)
        
        profile_list=list(chain(*profile_list))
    return render(request,'search.html',context={"user_profile":user_profile,"profile_list":profile_list})



@login_required(login_url="signin")
def profile(request,*args,**kwargs):
    user=request.user.username
    user_object=User.objects.get(username=kwargs.get("pk"))
    user_profile=Profile.objects.get(user=user_object)
    posts=Post.objects.filter(user=user_object)
    follower=FollowersCount.objects.filter(user=user_object.username,follower=user)
    my_followers=FollowersCount.objects.filter(user=user_object.username)
    my_followings=FollowersCount.objects.filter(follower=user_object)
    return render(request,'profile.html',context={"user_profile":user_profile,"posts":posts,"user_object":user_object,"user":user,"follower":follower,"my_followers":my_followers,"my_followings":my_followings})



@login_required(login_url="signin")
def follow(request,*args,**kwargs):
    if request.method=="POST":
        follower=request.user.username
        user=User.objects.get(username=kwargs.get("pk"))
        print("hello")
        if FollowersCount.objects.filter(follower=follower,user=user.username).first():
            delete_follower=FollowersCount.objects.filter(follower=follower,user=user.username)
            delete_follower.delete()
            return redirect('profile/'+str(user))
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user.username)
            new_follower.save()
            return redirect('profile/'+str(user))
    else:
        return redirect("/")


@login_required(login_url="signin")
def like_post(request,*args,**kwargs):
    user= request.user.username
    post_id=kwargs.get("pk")
    post=Post.objects.get(id=post_id)
    like_filter=LikePost.objects.filter(post_id=post_id,username=user).first() 
    if like_filter == None:
        new_like=LikePost.objects.create(post_id=post_id,username=user)
        new_like.save()
        post.likes=post.likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.likes=post.likes-1
        post.save()
        return redirect('/')


@login_required(login_url="signin")
def upload(request):
    if request.method=="POST":
        image=request.FILES.get('image_upload')
        caption=request.POST["caption"]
        user=request.user.username
        new_post=Post.objects.create(user=user,image=image,caption=caption,)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url="signin")
def settings(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get("image") == None:
            image = user_profile.profileimg
            bio =request.POST["bio"]
            location=request.POST["location"]

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        if request.FILES.get("image") != None:
            image=request.FILES.get("image")
            bio =request.POST["bio"]
            location=request.POST["location"]

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect("settings")
    return render(request,"setting.html",context={"user_profile":user_profile})


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            password2 = form.cleaned_data.get("password2")
            email=form.cleaned_data.get("email")
            username=form.cleaned_data.get("username")
#---------------check wheather email registered or not---------------------------------------

            if User.objects.filter(email=email).exists():
                messages.info(
                    request, 'An Account with this Email already Registered')
                return redirect('signup')

#---------------if password 1&2 are equal saveform and create a user and profile,if not error(password not matching)---------------------------------------

            elif password == password2:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                signup_user=User.objects.get(username=username)
#---------------log user in after signup-------------------------------------------
                user=authenticate(username=username,password=password)
                login(request,user)
#---------------create a profile for the user---------------------------------------
                new_profile=Profile.objects.create(user=signup_user,id_user=signup_user.id)
                new_profile.save()
                return redirect('settings')

            else:
                messages.info(request, "password not matching")
                return redirect('signup')

#----------------if form not valid ie.username exsists-------------------
        else:
            
            username = request.POST['username']

            if User.objects.filter(username=username).exists:
                messages.info(request, 'username Taken')
                return redirect('signup')
    else:
        return render(request, "signup.html", context={"form": form})

def signin(request):
    form=SigninForm()
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,'Credentials Invalid')
            return redirect("signin")
    return render(request,'signin.html',context={"form":form})

@login_required(login_url="signin")
def signout(request):
    logout(request)
    return redirect("signin")