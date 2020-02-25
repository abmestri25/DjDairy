from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import memory, ExtendedUser
from django.views.decorators.csrf import csrf_exempt

def login_url(request):
   
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
        
            return HttpResponseRedirect(reverse('show'))
        else:
            
            messages.info(request,"Invalid Credentials")
            return render(request,'login.html')
    else:
        
        return render(request,'login.html')

@login_required(login_url="login")
def logout_url(request):
    if request.method=="POST":
        logout(request)
        return HttpResponseRedirect(reverse('login'))

@login_required(login_url='/login/')
def show(request):
    details = ExtendedUser.objects.filter(user=request.user)
    memories = memory.objects.order_by('-date').filter(user=request.user)
    return render(request,'show.html',{'memories':memories , 'details':details})

@login_required(login_url="/login")
def add(request):
    if request.method == "POST": 
        data = request.POST['data'] 
        desc = request.POST['desc']
        new = memory(title = data,desc=desc,user=request.user)
        new.save()
        return render(request,'add.html')
    else:
        return render(request,'add.html')


def signup(request):
    if request.method == "POST":
        # if both password matches then
        if request.POST['password'] == request.POST['password1']: 
            # if user is already present
            try:
                user=User.objects.get(username=request.POST['username'])
                messages.info(request,"Username Has Already Taken")
                return render(request,'signup.html')

            #else create user
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],first_name= request.POST['first_name'],last_name= request.POST['last_name'],email=request.POST['email'])
                phone_no = request.POST['phone_no']
                age = request.POST['age']
                extenduser = ExtendedUser(phone_no=phone_no,age=age,user=user)
                extenduser.save()
                messages.info(request,"Signed Up Successfully")
                return render(request,'signup.html')

        else:
            messages.info(request,"Password don't match")
            return render(request,'signup.html')

    else:
        return render(request,'signup.html')

    return render(request,'signup.html')


@csrf_exempt
def delete_memory(request,mem_id):
    
    memory.objects.get(id=mem_id).delete()
    return HttpResponseRedirect('/show')