from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os
from django.conf import settings
from requests import session
from django.core.mail import send_mail
from random import randint
from .models import *

def home(request):
    videos = Videos.objects.all()
    videos = videos[:6:-1]
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=='POST'):
        try:
            email = request.POST.get('email')
            n = Newslater()
            n.email = email
            n.save()
        except:
            pass
        return HttpResponseRedirect('/')
    return render(request,"index.html",{'Videos':videos,'Maincategory':maincategory,'Subcategory':subcategory})
def exam(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(request,"exam.html",{'Maincategory':maincategory,'Subcategory':subcategory})
def About(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(request,"About.html",{'Maincategory':maincategory,'Subcategory':subcategory})
def blog(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(request,"blog.html",{'Maincategory':maincategory,'Subcategory':subcategory})
def teachers(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(request,"teacher.html",{'Maincategory':maincategory,'Subcategory':subcategory})

def event(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    return render(request,"event.html",{'Maincategory':maincategory,'Subcategory':subcategory})
def courses(request,num):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=='POST'):
        search = request.POST.get('search')
        videos = Videos.objects.filter(Q(name__icontains=search))
    else:
        videos = Videos.objects.filter(maincategory=Maincategory.objects.get(id=num))
    videos = videos[::-1]
    return render(request,"courses.html",{'Videos':videos,'Maincategory':maincategory,'Subcategory':subcategory})
def signup(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=="POST"):
        u = Student()
        u.name = request.POST.get("name")
        u.username = request.POST.get("username")
        u.email = request.POST.get("email")
        u.phone = request.POST.get("phone")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if(password==cpassword):
            try:
                user = User.objects.create_user(username=u.username,password=password,email=u.email)
                user.save()
                u.save()
                subject = 'Congratulations! Your Account Has been Created Successfully : Team NNU Digital University'
                message =  """
                                %s! Your Account Has Been Created Sucessfully! 
                                Thanks to create an account with Us.
                                Team : NNU Digital University
                                keep Connecting with us
                                http://localhost:8000                    
                           """%(u.name)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [u.email, ]
                send_mail( subject, message, email_from, recipient_list )
                messages.success(request,"Account Created...")
                return HttpResponseRedirect("/login/")
            except:
                messages.error(request,"User Name already Exists")
                return render(request,"signup.html")    
        else:
            messages.error(request,"Password and Confirm Password does not matched!!!!")
    return render(request,"signup.html",{'Maincategory':maincategory,'Subcategory':subcategory})

def login(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=='POST'):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid User Name or Password")
    return render(request,"login.html",{'Maincategory':maincategory,'Subcategory':subcategory})

@login_required(login_url='/login/')
def addvideo(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=="POST"):
        p = Videos()
        p.name = request.POST.get('name')
        p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
        p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
        p.description = request.POST.get('description')
        p.video = request.FILES.get('video')
        try:
            p.admin = Admin.objects.get(username=request.user)
        except:
            return HttpResponseRedirect("/profile/")
        p.save()
        subject = 'CheckOut Our Latest Videos on NNU Digital University : Team NNU Digital University'
        message =  """
                        Hey!
                        We upload Some more Latest Videos with best offerce 
                        please checkout
                        Thanks you 
                        Team : NNU Digital University
                        keep Touching with us
                        http://localhost:8000//singleproduct/%d                    
                   """%(p.id)
        email_from = settings.EMAIL_HOST_USER
        subscribers = Newslater.objects.all()
        for i in subscribers:
            recipient_list = [i.email,]
            send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect("/profile/")
    return render(request,"addvideo.html",{'Maincategory':maincategory,'Subcategory':subcategory})

def singlevideo(request,num):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    p = Videos.objects.get(id=num)
    videos = Videos.objects.all()
    videos = videos[:8:-1]
    return render(request,"singlevideo.html",{'Videos':p,'Video':videos,'Maincategory':maincategory,'Subcategory':subcategory})

@login_required(login_url='/login/')
def editvideo(request,num):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    try:
        p = Videos.objects.get(id=num)
        admin = Admin.objects.get(username=request.user)
        if(p.admin==admin):
            maincategory = Maincategory.objects.exclude(name=p.maincategory)
            subcategory = Subcategory.objects.exclude(name=p.subcategory)
            if(request.method=="POST"):
                p.name = request.POST.get('name')
                p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
                p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
                p.description = request.POST.get('description')
                if(request.FILES.get('video')):
                    p.video = request.FILES.get('video')
                p.save()
                return HttpResponseRedirect("/profile/")
            return render(request,"editvideo.html",{'Videos':p,'Maincategory':maincategory,'Subcategory':subcategory})
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")
    
@login_required(login_url='/login/')
def deletevideo(request,num):
    try:
        p = Videos.objects.get(id=num)
        admin = Admin.objects.get(username=request.user)
        if(p.admin==admin):
            p.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")
    
@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@login_required(login_url='/login/')
def profilePage(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            admin = Admin.objects.get(username=request.user)
            videos = Videos.objects.filter(admin=admin)
            videos = videos[::-1]
            return render(request,"adminprofile.html",{"User":admin,"Videos":videos,'Maincategory':maincategory,'Subcategory':subcategory})
        except:
            student = Student.objects.get(username=request.user)
            return render(request,"studentprofile.html",{"User":student,'Maincategory':maincategory,'Subcategory':subcategory})
        
@login_required(login_url='/login/')
def updateprofile(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            user = Student.objects.get(username=request.user)
        except:
            user = Admin.objects.get(username=request.user)
        if(request.method=="POST"):
            user.name=request.POST.get('name')
            user.email=request.POST.get('email')
            user.phone=request.POST.get('phone')
            user.addressline1=request.POST.get('addressline1')
            user.addressline2=request.POST.get('addressline2')
            user.addressline3=request.POST.get('addressline3')
            user.pin=request.POST.get('pin')
            user.city=request.POST.get('city')
            user.state=request.POST.get('state')
            if(request.FILES.get('pic')):
                if(user.pic):
                    os.remove("media/"+str(user.pic))
                user.pic=request.FILES.get('pic')
            user.save()
            return HttpResponseRedirect("/profile/")
    return render(request,"updateprofile.html",{"User":user,'Maincategory':maincategory,'Subcategory':subcategory})

def contact(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    try:
        if(request.method=='POST'):
            c = Contact()
            c.name = request.POST.get('name')
            c.email = request.POST.get('email')
            c.phone = request.POST.get('phone')
            c.subject = request.POST.get('subject')
            c.message = request.POST.get('message')
            c.save()
            subject = 'Your Query Has been Submitted : Team NNU Digital University'
            message =  """
                            Thanks to Share your Query with us
                            Our Team will Contact You Soon
                            Team : NNU Digital University
                            keep Connecting with us
                            http://localhost:8000                    
                       """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [c.email, ]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request,"Your Query Has Been Submitted Successfully! Our Team Will Contact You Soon!")
    except:
        HttpResponseRedirect('/contact/')
    return render(request,"contact.html",{'Maincategory':maincategory,'Subcategory':subcategory})

def forgetusername(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=='POST'):
        try:
            username = request.POST.get("username")
            user = User.objects.get(username=username)
            if(user is not None):
                try:
                    user = Admin.objects.get(username=username)
                except:
                    user = Student.objects.get(username=username)
                num = randint(100000,999999)
                request.session['otp']=num
                request.session['user']=username
                subject = 'OTP for Password Reset : Team NNU Digital University'
                message =  """
                                OTP : %d
                                Team : NNU Digital University
                                keep Connecting with us
                                http://localhost:8000                    
                           """%num
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/forgetotp/")
            else:
                messages.error(request,'Username not Found')
        except:
            messages.error(request,'Username not Found')
    return render(request,'forgetusername.html',{'Maincategory':maincategory,'Subcategory':subcategory})

def forgetotp(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=='POST'):
        otp = int(request.POST.get("otp"))
        sessionotp = request.session.get('otp',None)
        if(otp == sessionotp):                  
            return HttpResponseRedirect('/forgetpassword/')
        else:
            messages.error(request,'Invalid OTP') 
    return render(request,'forgetotp.html',{'Maincategory':maincategory,'Subcategory':subcategory})

def forgetpassword(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    if(request.method=='POST'):
        password = (request.POST.get("password"))
        cpassword = (request.POST.get("cpassword"))
        if(password == cpassword): 
            user = User.objects.get(username = request.session.get('user'))
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password and Confirm Doesn't Match")
    return render(request,'forgetpassword.html',{'Maincategory':maincategory,'Subcategory':subcategory})