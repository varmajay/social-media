import random
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from myapp.forms import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.urls import reverse


# Create your views here.
@login_required(login_url='/')  
def index(request):
    user = User.objects.filter(is_staff = False).exclude(id = request.user.id)
    followers = len(Follower.objects.filter(user = request.user))
    following = len(Follower.objects.filter(follower = request.user))
    fol = Follower.objects.filter(follower = request.user)[::-1]
    
    post =[]
    for data in fol:
        temp = Post.objects.filter(user__id = data.user.id)[::-1]
        for data1 in temp:
            # print(data1)
            post.append(data1)
    # print(post)

    if request.method =="POST":
        form = CreatepostForm(request.POST,request.FILES)

        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            messages.info(request,"Sucessfully POST ")
            return redirect('index')
        else:
            messages.info(request, form.errors)
            return redirect('index')

    else:
        form = CreatepostForm()

    return render(request,'index.html',{'form':form,'user':user,'followers':followers,'following':following,'post':post})



def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            subject = 'welcome to Social Media '
            message = f"""Hi {request.POST['name']}, thank you for registering in Social Media ."""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail( subject, message, email_from, recipient_list )
            form.save()
            messages.success(request,'Your Are Register Sucessfully')
            return redirect('login')
        else:
            messages.error(request,form.errors)
            return render(request,'register.html',{'form':form})
    else:
        form =RegisterForm()
    return render(request,'register.html',{'form':form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method =="POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(email = form.cleaned_data['email'],password = form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.info(request,'Invalid Email and Password')
                    return render(request,'login.html',{'form':form})
            messages.info(request,'Invalid Email and Password')
            return render(request,'login.html',{'form':form})
        else:
            form = LoginForm()
        return render(request,'login.html',{'form':form})


@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def forgot_password(request):
    if request.user.is_authenticated:   
        return redirect('index')
    else:
        if request.method =="POST":
            try:
                user=User.objects.get(email=request.POST['email'])
                # print(user)
                password="".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=9))
                # print(password)
                subject="Reset Password With Email Id"
                message=f""" hello {user.email} your new password is {password}"""
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'],]
                send_mail(subject,message,email_from,recipient_list)
                user.password=make_password(password)
                user.save()
                messages.success(request,'Your New password send to your email')
                return redirect('login')
            except:
                messages.warning(request,'Enter valid email address')
                return render(request,'forgot-password.html')
        return render(request,'forgot-password.html')




@login_required(login_url='/')
def setting(request):   
    if request.method =="POST":
        form1=PasswordForm(user=request.user,data=request.POST)
        if form1.is_valid():
            update_session_auth_hash(request,form1.user)
            form1.save()
            messages.success(request,'your password change successfully')
            return redirect('login')
        else:
            messages.warning(request,'enter the correct pasword')
            return render(request,'change-password.html',{'form':form})
    else:
        form=PasswordForm(user=request.user)
    return render(request,'profile-account-setting.html',{'form':form})

    
@login_required(login_url='/')
def profile(request):
    profile = User.objects.get(id =request.user.id)
    post = Post.objects.filter(user = request.user)
    followers = len(Follower.objects.filter(user=request.user))
    following = len(Follower.objects.filter(follower=request.user))
    return render(request,'profile.html',{'profile':profile,'post':post,'followers':followers,'following':following})


@login_required(login_url='/')
def edit_profile(request):
    if request.method =="POST":
        form=ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'your profile update')
            return redirect('edit-profile')
        else:
            # print(form.errors)
            messages.warning(request,'Enter the valid data')
            return render(request,'edit-profile.html',{'form':form})
    else:
        form=ProfileForm(instance=request.user)
    return render(request,'edit-profile.html',{'form':form})



def search(request):
    if request.method =="GET":
        search=request.GET.get('search')
        if search:
            user=User.objects.filter(name__icontains=search)
            # print(user)
            return render(request,'search.html',{'user':user})
        else:
            return redirect('index')
    # print(user)
    return render(request,'search.html',{'user':user})


def edit_post(request,pk):
    uid = Post.objects.get(id=pk)
    if request.method =="POST":
        form = EditpostForm(request.POST,instance=uid)
        if form.is_valid():
            form.save()
            messages.success(request,'your post is update')
            return redirect('profile')
        else:
            messages.warning(request,'Enter the valid data')
            return render(request,'edit-profile.html',{'form':form})
    else:
        form = EditpostForm(instance=uid)
    return render(request,'edit-post.html',{'uid':uid,'form':form})


def delete_post(request,pk):
    post = Post.objects.get(id=pk)
    post.delete()
    messages.info(request,"Post deleted.")
    return redirect('profile') 



def view_profile(request,pk):
    user = User.objects.get(id=pk)
    post = Post.objects.filter(user = user)
    follower = request.user
    if Follower.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    followers = len(Follower.objects.filter(user=pk))
    following = len(Follower.objects.filter(follower=pk))

    # if request.method == 'POST':
    #     user = request.POST['user']
    #     follower = request.POST['follower']
    #     uid_user = User.objects.get(id = request.POST['user'])
    #     uid_follower = User.objects.get(id = request.POST['follower'])
    #     # print(uid_follower.id)
    #     # print(uid_user.id)


    #     if Follower.objects.filter(user__id = user, follower__id = follower).first():
    #         delete_follower = Follower.objects.get(user__id = user, follower__id = follower)
    #         delete_follower.delete()
    #         return render(request,'view-profile.html',{'post':post,'user':user,'button_text':button_text,'followers':followers,'following':following})
    #     else:
    #         new_follower = Follower.objects.create(user = uid_user, follower = uid_follower)
    #         new_follower.save()
    #         return render(request,'view-profile.html',{'post':post,'user':user,'button_text':button_text,'followers':followers,'following':following}))

    return render(request,'view-profile.html',{'post':post,'user':user,'button_text':button_text,'followers':followers,'following':following})




def follow(request):
    if request.method == 'POST':
        user = request.POST['user']  
        follower = request.POST['follower']
        uid_user = User.objects.get(id = request.POST['user'])
        uid_follower = User.objects.get(id = request.POST['follower'])
        # print(uid_follower.id)
        # print(uid_user.id)


        if Follower.objects.filter(user__id = user, follower__id = follower).first():
            delete_follower = Follower.objects.get(user__id = user, follower__id = follower)
            delete_follower.delete()
            return redirect('/view-profile/'+user)
        else:
            new_follower = Follower.objects.create(user = uid_user, follower = uid_follower)
            new_follower.save()
            return redirect('/view-profile/'+user)
    else:
        return redirect('view-profile/')    




def like_post_profile(request):
    user = request.user
    post_id = request.GET.get('post_id')
    # print(type(post_id))
    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(post = post, user = user).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post = post, user = user)
        new_like.save()
        post.likes = post.likes+1
        post.save()
        return redirect('view-profile/'+post_id)
    else:
        like_filter.delete()
        post.likes = post.likes-1
        post.save()
        return redirect('view-profile/'+post_id)



def like_post(request):
    user = request.user
    post_id = request.GET.get('post_id')
    # print(type(post_id))
    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(post = post, user = user).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post = post, user = user)
        new_like.save()
        post.likes = post.likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.likes = post.likes-1
        post.save()
        return redirect('/')



    

def comment(request,pk):
    post = Post.objects.get(id = pk)
    user = request.user
    comment = request.POST['comment']
    # print(post)
    # print(request.user)
    # print(comment)
    if request.method =="POST":
        Comment.objects.create(user=user, post=post, comment = comment)
    return redirect('index')



def view_comment(request,pk):
    uid = Post.objects.get(id =pk)
    comment = Comment.objects.filter(post__id = uid.id)
    
    return render(request,'view-comment.html',{'comment':comment})