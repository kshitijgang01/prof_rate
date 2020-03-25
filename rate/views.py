from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Professors,Courses,Employee,Prof_to_subj,ProfRating,ProfReview,CourseRating,CourseReview,Complaints
from django.contrib.auth.models import User, auth
from .forms import LoginForm
from django.db.models import Avg
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from random import seed
from random import random
from django.core.mail import EmailMessage
import string
# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username,password=password)
        if user is not None :
            today = date.today()
            emp=Employee.objects.get(user=user)
            block_date=emp.block_date
            if block_date is not None or emp.is_blocked==True:
                block_date=emp.block_date.date()
                if (block_date-today).days > 0 or emp.is_blocked==True :
                    messages.info(request, "you are blocked")
                    return redirect('login')
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "invalid credentials")
            return redirect('login')
    else:
        return render(request, 'rate/login.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        id_=request.POST['id']
        department=request.POST['department']
        img_src=request.POST['img_src']
        password=request.POST['password']
        password_repeat=request.POST['password1']
        if password != password_repeat :
            messages.info(request, 'password not same')
            return redirect('register')
        seed(1)
        chars = str(int(random()*100000))
        email = EmailMessage(
        subject='code',
        body=chars,
        from_email='kshitijgang76@zohomail.in',
        to=[username],
        reply_to=['kshitijgang76@zohomail.in'],
        headers={'Content-Type': 'text/plain'},
        )
        email.send()
        user=User.objects.create_user(username=username,password=password_repeat,first_name=firstname,last_name=lastname,)
        user.save()
        employee=Employee.objects.create(user=user,id=id_,user_photo=img_src,department=department,is_blocked=True)
        employee.save()
        auth.login(request, user)
        return redirect('confirm')
    else :
        return render(request,'rate/register.html')

def confirmation(request):
    user=request.user
    if request.method=="POST":
        con=request.POST['1']
        seed(1)
        if con == random() :
            employee=Employee.objects.get(user=user)
            employee.is_blocked=False
            employee.save()
            auth.logout(request) 
            return redirect('login')
        else:
            messages.info(request,'Did not match')
            return redirect('confirm')
    else:
        return (render(request,'rate/con.html'))


        
def logout(request):
    auth.logout(request) 
    return redirect('/')      




def index(request):
    return render(request, 'rate/index.html')

def prof(request):
    all_prof=Professors.objects.all()
    a=[]
    for prof in all_prof:
        a.append(prof)
    return render(request, 'rate/profInfo.html',{'a':a})

def course(request,):
    course_info=Courses.objects.all()
    a=[]
    for prof in course_info:
        a.append(prof)
    
    return render(request, 'rate/course.html',{'a':a})

def my_view(request):
    login_data = request.POST.dict()
    username = login_data.get['username']
    password = login_data.get['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'rate/mypage.html',{'user':user})
        
    else:
        return render(request,'rate/course.html')
        

def detail(request,prof_name):
    user=request.user
    if request.method=='POST':
        one=request.POST['1']
        two=request.POST['2']
        three=request.POST['3']
        four=request.POST['4']
        five=request.POST['5']
        six=request.POST['6']
        seven=request.POST['7']
        print(seven)

        check=ProfRating.objects.filter(prof_own__prof_name=prof_name,user__username=user.username)
        if check:
            '''print(check[0])
            check[0]['prof_grading_own']=one
            print(check[0])
            check[0].prof_puntuality_own=two
            check[0].prof_strictness_rating_own=three
            check[0].prof_teaching_skill_own=four
            check[0].prof_enthusiasm_own=five
            check[0].prof_overall_own=six
            print("laugh")
            check[0].save()
            print(check[0].prof_grading_own)'''
            prof_own=check[0].prof_own
            check[0].delete()
            rating=ProfRating.objects.create(user=user,prof_own=prof_own,prof_grading_own=one,prof_puntuality_own=two,prof_strictness_rating_own=three,prof_teaching_skill_own=four,prof_enthusiasm_own=five,prof_overall_own=six)
            rating.save()
        else:
            prof_own=Professors.objects.get(prof_name=prof_name)
            rating=ProfRating.objects.create(user=user,prof_own=prof_own,prof_grading_own=one,prof_puntuality_own=two,prof_strictness_rating_own=three,prof_teaching_skill_own=four,prof_enthusiasm_own=five,prof_overall_own=six)
            rating.save()
        if seven != '':    
            check_1=ProfReview.objects.filter(prof_own__prof_name=prof_name,user__username=user.username)
            if check_1:
                prof_own=check_1[0].prof_own
                check_1[0].delete()
                review=ProfReview.objects.create(user=user,prof_own=prof_own,prof_review_own=seven)
                review.save()
            else:
                prof_own=Professors.objects.get(prof_name=prof_name)
                review=ProfReview.objects.create(user=user,prof_own=prof_own,prof_review_own=seven)
                review.save()





        return redirect('detail',prof_name=prof_name)
    else:
        prof=Professors.objects.get(prof_name=prof_name)
        subject=Prof_to_subj.objects.filter(professor__prof_name=prof_name)
        b=subject
    
        form_boolean=False
        d=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_grading_own'))
        e=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_puntuality_own'))
        f=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_grading_own'))
        g=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_strictness_rating_own'))
        h=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_teaching_skill_own'))
        i=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_enthusiasm_own'))
        j=ProfRating.objects.filter(prof_own__prof_name=prof_name).aggregate(Avg('prof_overall_own'))
        y=ProfReview.objects.filter(prof_own__prof_name=prof_name)
        k=ProfReview.objects.filter(prof_own__prof_name=prof_name,user__username=user.username)
        k=k[0]
        print(k)
        cond=None
        if user is not None :
            cond=ProfRating.objects.filter(prof_own__prof_name=prof_name,user__username=user.username)
            if cond.exists():
                kj=0
            else:
                cond=[None]
            form_boolean=True


            
            


        
        return render(request, 'rate/detail.html',{'a':prof,'b':b,'d':d,'e':e,'f':f,'g':g,'h':h,'i':i,'j':j,'cond':cond[0],'k':k,'y':y})






def course_detail(request,course_id):
    user=request.user
    if request.method=='POST':
        one=request.POST['1']
        two=request.POST['2']
        three=request.POST['3']
        
        seven=request.POST['7']
        print(seven)

        check=CourseRating.objects.filter(course_own__course_id=course_id,user__username=user.username)
        if check:
            
            course_own=check[0].course_own
            check[0].delete()
            rating=CourseRating.objects.create(user=user,course_own=course_own,course_difficulty_own=one,course_content_rating_own=two,course_workload_own=three)
            rating.save()
        else:
            course_own=Courses.objects.get(course_id=course_id)
            rating=CourseRating.objects.create(user=user,course_own=course_own,course_difficulty_own=one,course_content_rating_own=2,course_workload_own=3)
            rating.save()
        if seven != '':    
            check_1=CourseReview.objects.filter(course_own__course_id=course_id,user__username=user.username)
            if check_1:
                course_own=check_1[0].course_own
                check_1[0].delete()
                review=CourseReview.objects.create(user=user,course_own=course_own,course_review_own=seven)
                review.save()
            else:
                course_own=Courses.objects.get(course_id=course_id)
                review=CourseReview.objects.create(user=user,course_own=course_own,course_review_own=seven)
                review.save()





        return redirect('course_detail',course_id=course_id)
    else:
        course=Courses.objects.get(course_id=course_id)
        prof=Prof_to_subj.objects.filter(subject__course_id=course_id)
        b=prof
    
        form_boolean=False
        d=CourseRating.objects.filter(course_own__course_id=course_id).aggregate(Avg('course_difficulty_own'))
        e=CourseRating.objects.filter(course_own__course_id=course_id).aggregate(Avg('course_workload_own'))
        f=CourseRating.objects.filter(course_own__course_id=course_id).aggregate(Avg('course_content_rating_own'))
        
        y=CourseReview.objects.filter(course_own__course_id=course_id)
        print(y[0])
        k=None
        
        cond=None
        if user is not None :
            cond=CourseRating.objects.filter(course_own__course_id=course_id,user__username=user.username)
            k=CourseReview.objects.filter(course_own__course_id=course_id,user__username=user.username)
            print(k)
            if k is not None :
                k=k[0]
            else:
                k=[None]
            if cond.exists():
                kj=0
            else: messages.info(request,'no such user')
            


            
            


        
        return render(request, 'rate/course_detail.html',{'a':course,'b':b,'d':d,'e':e,'f':f,'cond':cond[0],'k':k,'y':y})

def complaints(request):
    user=request.user
    if request.method=='POST':
        user_reported=request.POST['username']
        complaint=request.POST['text']
        a=User.objects.get(username=user_reported)
        if a  is None:
            messages.info(request,'no such user')
        else:
            a=Complaints.objects.create(user=user,user_to_be_reported=a,text=complaint)
            a.save()
            messages.info(request,'succesfully registerd a complaint')
            return redirect('complaints')
    else:
        return render(request, 'rate/compalaint.html')


            


