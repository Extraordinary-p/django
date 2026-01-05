from django.shortcuts import render,redirect
from django.http import HttpResponse
from random import sample
from first.models import *
# Create your views here.

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