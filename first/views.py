from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from random import sample
from first.models import *
# Create your views here.
from first.utils import *

def show_subjects(request):
    subejects = Subject.objects.all().order_by('no')
    return render(request,'subject.html',{'subjectVies':subejects})

def show_teachers(request):
    try:
        sno = int(request.GET.get('sno'))
        teachers = []
        if sno:
            subject_name = Subject.objects.only('name').get(no=sno)
            # 这里相当于拿到Subject模型中的一个对象
            teachers = Teacher.objects.filter(subject=subject_name)
        #     后续从对象中取值
        return render(request, 'teacher.html', {
            'subject': subject_name,
            'teachers': teachers
        })
    except (ValueError, Subject.DoesNotExist):
        return redirect('/')
def praise_or_criticize(request: HttpRequest) -> HttpResponse:
    if request.session.get('userid'):
        try:
            tno = int(request.GET.get('tno'))
            teacher = Teacher.objects.get(no=tno)
            if request.path.startswith('/praise/'):
                teacher.good_count += 1
                count = teacher.good_count
            else:
                teacher.bad_count += 1
                count = teacher.bad_count
            teacher.save()
            data = {'code': 20000, 'mesg': '投票成功', 'count': count}
        except (ValueError, Teacher.DoesNotExist):
            data = {'code': 20001, 'mesg': '投票失败'}
    else:
        data = {'code': 20002, 'mesg': '请先登录'}
    return JsonResponse(data)

def login(request: HttpRequest) -> HttpResponse:
    hint = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            password = gen_md5_digest(password)
            user = User.objects.filter(username=username, password=password).first()
            if user:
                request.session['userid'] = user.no
                request.session['username'] = user.username
                return redirect('/')
            else:
                hint = '用户名或密码错误'
        else:
            hint = '请输入有效的用户名和密码'
    return render(request, 'login.html', {'hint': hint})

def get_captcha(request: HttpRequest) -> HttpResponse:
    """验证码"""
    captcha_text = gen_random_code()
    request.session['captcha'] = captcha_text
    image_data = Captcha.instance().generate(captcha_text)
    return HttpResponse(image_data, content_type='image/png')

def logout(request):
    """注销"""
    request.session.flush()
    return redirect('/')