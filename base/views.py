from xml.dom import minicompat
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from manager.models import Manager
from contact.models import cont
from django.contrib.auth.models import User
import smtplib as s
from email.message import EmailMessage as e
import random
import string
from .models import Rooms,Reservation
import datetime
from django.db.models import Q



from .models import Rooms


# Create your views here.
def first(request):
    if not request.user.is_authenticated:
        return redirect('using')
    return render(request,'front/home.html')
def image(request):
    if not request.user.is_authenticated:
        return redirect('using')
    return render(request,'front/image.html')    
def panel(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm=0
    for i in request.user.groups.all():
        if i.name=="masteruser":
            perm=1
    if perm==0:
         error="Access denied"
         return render(request,"back/error.html",{'error':error})    
    return render(request,'back/panel.html')
def roominfo(request):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm=0
    for i in request.user.groups.all():
        if i.name=="masteruser":
            perm=1
    if perm==0:
         error="Access denied"
         return render(request,"back/error.html",{'error':error})     
    room=Rooms.objects.all()
    return render(request,'back/roominfo.html',{'room':room})  
def room(request):
    # to check if user is logged in or not
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm=0
    for i in request.user.groups.all():
        if i.name=="masteruser":
            perm=1
    if perm==0:
         error="Access denied"
         return render(request,"back/error.html",{'error':error})      
    if request.method=="POST":
       block=request.POST.get('block')
       type=request.POST.get('type')
       roomno=request.POST.get('roomno')
       capacity1=request.POST.get('capacity')
       available=request.POST.get('avail')
       if block=="" or type=="" or roomno=="" or available=="" or capacity1=="":
           error="Please fill all input field as evrything is necessary"
           return render(request,"back/error.html",{'error':error})
       createdslot=Rooms(Block=block,Type=type,Roomno=roomno,capacity=capacity1,Availability=available)   
       createdslot.save()
        

    
    return render(request,'back/room.html')  
    

def edit(request,pk):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm=0
    for i in request.user.groups.all():
        if i.name=="masteruser":
            perm=1
    if perm==0:
         error="Access denied"
         return render(request,"back/error.html",{'error':error})     
    if len(Rooms.objects.filter(pk=pk))==0:
        error="info not found"
        return render(request,"back/error.html",{'error':error})

    editing=Rooms.objects.get(pk=pk)
    if request.method=="POST":
       block=request.POST.get('block')
       type=request.POST.get('type')
       roomno=request.POST.get('roomno')
       capacity1=request.POST.get('capacity')
       available=request.POST.get('avail')
       if block=="" or type=="" or roomno=="" or available=="" or capacity1=="":
           error="Please fill all input field as evrything is necessary"
           return render(request,"back/error.html",{'error':error})
       editing.Block=block
       editing.Type=type
       editing.Roomno=roomno
       editing.capacity=capacity1
       editing.Availability=available
       
       editing.save()

    

    
    return render(request,'back/edit.html',{'pk':pk,'editing':editing })
def deleting(request,pk):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    perm=0
    for i in request.user.groups.all():
        if i.name=="masteruser":
            perm=1
    if perm==0:
         error="Access denied"
         return render(request,"back/error.html",{'error':error})     
    b=Rooms.objects.filter(pk=pk)
    b.delete()


    return redirect('info')
def mylogin(request):
    if request.method=="POST":
        username1=request.POST.get('username')
        passingword=request.POST.get('password')
        
        
        
        
        if username1!="" and passingword!="":
            user=authenticate(username=username1,password=passingword)
            #if user doesnot exist then none is return and if it exist its information stores in that variable user  
            if user!=None:
                login(request,user)#login request for that user
                return redirect('panel')
            else:
                error="Please fill valid user and password"
                return render(request,"back/error.html",{'error':error})  


        elif  username1=="" or passingword=="": 
            error="Please fill all input field as evrything is necessary"
            return render(request,"back/error.html",{'error':error})      
            


    return render(request,'back/mylogin.html') 


def mylogout(request):
    logout(request)

    return redirect('mylogin')
def contacting(request):
    return render(request,'front/contact.html')



# normal users,login,register,forgot password    
def userslogin(request):
    if request.method=="POST":
        username1=request.POST.get('username')
        passingword=request.POST.get('password')
        
        
        
        
        if username1!="" and passingword!="":
            user=authenticate(username=username1,password=passingword)
            #if user doesnot exist then none is return and if it exist its information stores in that variable user  
            if user!=None:
                login(request,user)#login request for that user
                w=request.user.email
                print(w)
                email=e()
        
                email['from']='21BCS110'
                email['to']=w
                email['subject']='logging into account'
                email.set_content("you are logged into your account")
                with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                       smtp.ehlo()
                       smtp.starttls()
                       smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                       smtp.send_message(email)
                return redirect('first')
            else:
                error="Please fill valid user and password"
                return render(request,"front/erroring.html",{'error':error})  


        elif  username1=="" or passingword=="": 
            error="Please fill all input field as evrything is necessary"
            return render(request,"front/erroring.html",{'error':error})      
            


    return render(request,'front/userslogin.html') 

def userloggingout(request):
    logout(request)

    return redirect('using')


def userregistering(request):
    if request.method=="POST":
        name=request.POST.get('name')
        username1=request.POST.get('uname')
        passingword1=request.POST.get('password1')
        passingword2=request.POST.get('password2')
        email=request.POST.get('email')

        if passingword1!=passingword2:
            error="please input same password and verify password"
            return render(request,"front/erroring.html",{'error':error})  
        

        count1=0 
        count2=0 
        count3=0 
        count4=0 
        for i in passingword1:
            if i>='0' and i<='9':
                count1=1   
            if i>='A' and i<='Z':
                count2=1  
            if i>='a' and i<='z':
                count3=1  
            if i in ['!','@','#','$','%','^','&','*','(',')']:
                count4=1
        if count1==0 or count2==0 or count3==0 or count4==0:
            warn="your password is not strong"
            return render(request,"front/erroring.html",{'warn':warn}) 
        if(len(passingword1)<8):
            warn="your password must contain minimum 8 character"
            return render(request,"front/erroring.html",{'warn':warn})
        if(len(User.objects.filter(username=username1))==0) and (len(User.objects.filter(email=email))==0):
            user=User.objects.create_user(username=username1,email=email,password=passingword1) 
            b=Manager(name=name,utxt=username1,email=email)
            b.save()  
            w=email
            print(w)
            email=e()
        
            email['from']='21BCS110'
            email['to']=w
            email['subject']='registering  into account'
            email.set_content("congrats!you are registerd now!! ")
            with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                       smtp.ehlo()
                       smtp.starttls()
                       smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                       smtp.send_message(email)  
           
            


    return render(request,'front/userslogin.html') 



def changingpassword(request):
    N = 5
  
 
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    print(res)
    global mini
    mini=res   
    if request.method=="POST":
        global email1
        email1=request.POST.get('reminder-email')
        print(email1)
        email=e()
        
        email['from']='21BCS110'
        email['to']=email1
        email['subject']='changing the password'
        email.set_content(mini)
        with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                 smtp.ehlo()
                 smtp.starttls()
                 smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                 smtp.send_message(email)
    return render(request,'front/plussing.html')    


def plussing(request):
    if request.method=="POST":
        verify1=request.POST.get('verify')
        newpass=request.POST.get('set')
        print(verify1,newpass,mini)
        if verify1!=mini:
            warn="enter correct verifying pass"
            return render(request,"front/erroring.html",{'error':warn}) 
        count1=0 
        count2=0 
        count3=0 
        count4=0 
        for i in newpass:
            if i>='0' and i<='9':
                count1=1   
            if i>='A' and i<='Z':
                count2=1  
            if i>='a' and i<='z':
                count3=1  
            if i in ['!','@','#','$','%','^','&','*','(',')']:
                count4=1
        if count1==0 or count2==0 or count3==0 or count4==0:
            warn="your password is not strong"
            return render(request,"front/erroring.html",{'error':warn}) 
        if(len(newpass)<8):
            warn="your password must contain minimum 8 character"
            return render(request,"front/erroring.html",{'error':warn}) 
        a=User.objects.get(email=email1)
        print(a)
        a.set_password(newpass)
        a.save()







    return render(request,'front/bethechange.html')


def roomstatus(request):
    curr=datetime.datetime.now()
    quer=Reservation.objects.filter(endtime__lte=curr)
    for i in quer:
            q=i.block
            r=i.number
            x=Rooms.objects.get(Block=q,Roomno=r)
            if(x.Availability=="Unavailable"):
                x.Availability="Available"
                x.save()
            i.delete()

    room=Rooms.objects.all().order_by('Availability')

    return render(request,"front/roomstatus.html", {'room':room}) 


def roombookingform(request):
    pass
# admin site logic
def requestedroom(request):
    requesting=Reservation.objects.all()
    return render(request,"back/requested.html",{'requesting':requesting}) 
def createdform(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        purpose=request.POST.get('purpose')
        roomno=request.POST.get('roomno')
        block=request.POST.get('blocking')
        de=request.POST.get('de')
        t1=request.POST.get('starttime')
        t2=request.POST.get('endtime')
        d1=request.POST.get('datestart')
        d2=request.POST.get('dateend')
        print(username,email,purpose,block,t1,t2,d1,d2)
        if(d1>d2):
            error="please choose correct startdate and enddate"
            return render(request,"front/erroring.html",{'error':error})
        if(d1==d2 and t1>t2):
            error="please choose correct startdate and enddate"
            return render(request,"front/erroring.html",{'error':error})
        dto1= datetime.datetime.strptime(d1, '%Y-%m-%d').date()    
        dto2= datetime.datetime.strptime(d2, '%Y-%m-%d').date() 
        print(type(dto1))
        tto1=datetime.datetime.strptime(t1,'%H:%M').time()
        tto2=datetime.datetime.strptime(t2,'%H:%M').time()
        print(tto1)
        dt1=datetime.datetime.combine(dto1,tto1)
        dt2=datetime.datetime.combine(dto2,tto2)
        print(dt1)
        current=datetime.datetime.now()
        print(current) 
        print(dt1>dt2)
        quer=Reservation.objects.filter(endtime__lte=current)
        for i in quer:
            q=i.block
            r=i.number
            x=Rooms.objects.get(Block=q,Roomno=r)
            if(x.Availability=="Unavailable"):
                x.Availability="Available"
                x.save()
            i.delete()
                 
            







        x=Rooms.objects.filter(Block=block,Roomno=roomno) 
        if(len(x)==0):
            error="Please input valid room number."
            return render(request,"front/erroring.html",{'error':error})
        for i in x:
            if i.Availability=="Unavailable" :
                error="sorry it is unavailable"
                return render(request,"front/request.html",{'result':error})
        myrequest=Reservation(user=User.objects.get(username=username),check_in=dt1,endtime=dt2,block=block,number=roomno,purpose=purpose, Desgination=de)
        myrequest.save()   
        email=e()
        
        email['from']='21BCS110'
        email['to']='shindesamarth19@gmail.com'
        email['subject']='new room request has been updated'
        email.set_content("pending request")
        with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                       smtp.ehlo()
                       smtp.starttls()
                       smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                       smtp.send_message(email)      
        result="your request for room has been accepted"               
        return render(request,"front/re.html",{'result':result})


    




    return render(request,"front/suggest.html")      


def accept(request,pk):
    d=Reservation.objects.filter(pk=pk)
    for i in d:
       m=i.block
       n=i.number
       d=i.user
    r=User.objects.filter(username=d)
    for i in r:
        w=i.email

    rom=Rooms.objects.get(Roomno=n,Block=m)
    rom.Availability="Unavailable"
    rom.save()
    
    print(w)
    email=e()
        
    email['from']='21BCS110'
    email['to']=w
    email['subject']='accepting the request'
    email.set_content("your request for room has been accepted ")
    with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                       smtp.ehlo()
                       smtp.starttls()
                       smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                       smtp.send_message(email)  



    return redirect('requested') 

def declined(request,pk):
    declinetart=Reservation.objects.filter(pk=pk)
    for i in declinetart:
       q=i.user
    r=User.objects.filter(username=q)
    for i in r:
        w=i.email   
    

    print(w)
    email=e()
        
    email['from']='21BCS110'
    email['to']=w
    email['subject']='decliningthe request'
    email.set_content("your request for room has been declined ")
    with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                       smtp.ehlo()
                       smtp.starttls()
                       smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                       smtp.send_message(email)
    declinetart.delete()
    return redirect('requested')




def answer(request,pk):
    if not request.user.is_authenticated:
        return redirect('mylogin')
    if request.method=="POST":
        msg=request.POST.get('message')
        print(msg)
        ret=cont.objects.get(pk=pk)
        print(ret.email)
        w=ret.email
        email=e()
        
        email['from']='21BCS110'
        email['to']=w
        email['subject']='message'
        email.set_content(msg)
        with s.SMTP(host ='smtp.gmail.com',port=587) as smtp:
                       smtp.ehlo()
                       smtp.starttls()
                       smtp.login('21bcs110@iiitdwd.ac.in','cqidtruxzsxarlfn')
                       smtp.send_message(email)
        return redirect('contactinfo')               

    
    return render(request,"back/mess.html",{'pk':pk})    
    

       

    


 