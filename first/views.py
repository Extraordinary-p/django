from django.core.serializers import serialize
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from random import sample
from first.models import *
# Create your views here.
from first.utils import *
from bpmappers.djangomodel import ModelMapper
from rest_framework.decorators import api_view
from rest_framework.response import Response

from first.models import Subject
from rest_framework import serializers

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'

class SubjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('no', 'name')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        exclude = ('subject', )

# def show_subjects(request):
#     subejects = Subject.objects.all().order_by('no')
#     return render(request,'subject.html',{'subjectVies':subejects})

@api_view(['GET'])
def show_subject(request:HttpRequest) -> HttpResponse:
    subject = Subject.objects.all().order_by('no')
    serializer = SubjectSerializer(subject,many=True)
    return Response(serializer.data)


# 视图函数，处理获取教师信息的请求
@api_view(('GET',))  # 只允许 GET 请求
def show_teachers(request: HttpRequest) -> HttpResponse:
    try:
        # 获取请求参数 '1'，并转换为整数
        sno = 1
        # 根据学科编号 (sno) 查询学科，获取学科名称（仅取'name'字段）
        subject = Subject.objects.only('name').get(no=3)
        # 查询与该学科相关的教师，排除 subject 字段，并按教师编号排序
        teachers = Teacher.objects.filter(subject=subject).order_by('no')
        # 将查询到的学科数据通过序列化器进行序列化
        subject_seri = SubjectSimpleSerializer(subject)
        # 将查询到的教师数据通过序列化器进行序列化（多个教师）
        teacher_seri = TeacherSerializer(teachers, many=True)
        # 返回 API 响应，包含学科数据和教师数据
        return Response({'teachers': teacher_seri.data})
    # 捕获异常，处理可能出现的错误情况
    except (TypeError, ValueError, Subject.DoesNotExist):
        # 如果发生异常，返回 404 状态码
        return Response(status=404)



# def show_teachers(request):
#     try:
#         sno = int(request.GET.get('sno'))
#         teachers = []
#         if sno:
#             subject_name = Subject.objects.only('name').get(no=sno)
#             # 这里相当于拿到Subject模型中的一个对象
#             teachers = Teacher.objects.filter(subject=subject_name)
#         #     后续从对象中取值
#         return render(request, 'teacher.html', {
#             'subject': subject_name,
#             'teachers': teachers
#         })
#     except (ValueError, Subject.DoesNotExist):
#         return redirect('/')
# def praise_or_criticize(request: HttpRequest) -> HttpResponse:
#     if request.session.get('userid'):
#         try:
#             tno = int(request.GET.get('tno'))
#             teacher = Teacher.objects.get(no=tno)
#             if request.path.startswith('/praise/'):
#                 teacher.good_count += 1
#                 count = teacher.good_count
#             else:
#                 teacher.bad_count += 1
#                 count = teacher.bad_count
#             teacher.save()
#             data = {'code': 20000, 'mesg': '投票成功', 'count': count}
#         except (ValueError, Teacher.DoesNotExist):
#             data = {'code': 20001, 'mesg': '投票失败'}
#     else:
#         data = {'code': 20002, 'mesg': '请先登录'}
#     return JsonResponse(data)
#
# def login(request: HttpRequest) -> HttpResponse:
#     hint = ''
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if username and password:
#             password = gen_md5_digest(password) #转成md5字符串
#             user = User.objects.filter(username=username, password=password).first()
#             if user:
#                 request.session['userid'] = user.no
#                 request.session['username'] = user.username
#                 return redirect('/')
#             else:
#                 hint = '用户名或密码错误'
#         else:
#             hint = '请输入有效的用户名和密码'
#     return render(request, 'login.html', {'hint': hint})
#
# def get_captcha(request: HttpRequest) -> HttpResponse:
#     """验证码"""
#     captcha_text = gen_random_code()
#     request.session['captcha'] = captcha_text
#     image_data = Captcha.instance().generate(captcha_text)
#     return HttpResponse(image_data, content_type='image/png')
#
# def logout(request):
#     """注销"""
#     request.session.flush()
#     return redirect('/')
#
# # 导出excel
# import xlwt
# from urllib.parse import quote
# def export_teachers_excel(request):
#     # 创建工作簿
#     wb = xlwt.Workbook()
#     # 添加工作表
#     sheet = wb.add_sheet('老师信息表')
#     # 从数据库中查询所有 Teacher 模型的记录，返回一个 QuerySet 对象
#     queryset = Teacher.objects.all()
#
#     # 定义 Excel 表格的表头（列名），用于显示给用户看的中文标题
#     colnames = ('姓名', '介绍', '好评数', '差评数', '学科')
#
#     # 遍历表头元组 colnames，使用 enumerate 同时获取索引（列号）和值（中文列名）
#     for index, name in enumerate(colnames):
#         # 在 Excel 的第 0 行（即第一行）写入表头：
#         #   - 第一个参数 0：表示写入第 0 行（Excel 行号从 0 开始）
#         #   - 第二个参数 index：表示写入第 index 列（A=0, B=1, C=2...）
#         #   - 第三个参数 name：要写入的实际文本（如“姓名”）
#         sheet.write(0, index, name)
#
#     # 定义与表头对应的模型字段名（属性名），顺序必须与 colnames 一一对应
#     props = ('name', 'detail', 'good_count', 'bad_count', 'subject')
#
#     # 遍历所有教师数据（queryset），enumerate 返回 (行索引, 教师对象)
#     # 注意：row 从 0 开始，但 Excel 数据行应从第 1 行开始（因为第 0 行是表头）
#     for row, teacher in enumerate(queryset):
#         # 再次遍历每个字段名（props），获取列索引 col 和字段名 prop
#         for col, prop in enumerate(props):
#             # 从当前 teacher 对象中动态获取名为 prop 的属性值；
#             # 如果该属性不存在，则返回空字符串 ''（避免 AttributeError）
#             value = getattr(teacher, prop, '')
#
#             # 特殊处理：如果获取到的 value 是 Subject 模型的实例（例如 subject 是外键）
#             # 则将其转换为该 Subject 对象的 name 属性（比如学科名称字符串）
#             if isinstance(value, Subject):
#                 value = value.name  # 假设 Subject 模型有一个 name 字段
#
#             # 将最终的 value 写入 Excel 单元格：
#             #   - 行号：row + 1（因为第 0 行是表头，数据从第 1 行开始）
#             #   - 列号：col（与 props 中的字段顺序一致）
#             #   - 值：value（可能是字符串、数字，或已转换的学科名称）
#             sheet.write(row + 1, col, value)
#     # 保存Excel
#     buffer = BytesIO()
#     wb.save(buffer)
#     # 将二进制数据写入响应的消息体中并设置MIME类型
#     resp = HttpResponse(buffer.getvalue(), content_type='application/vnd.ms-excel')
#     # 中文文件名需要处理成百分号编码filename = quote('老师.xls')
#     filename = quote('老师.xls')
#     # 通过响应头告知浏览器下载该文件以及对应的文件名
#     resp['content-disposition'] = f'attachment; filename*=utf-8\'\'{filename}'
#     return resp
# #生成柱状图
# def get_teachers_data(request):
#     queryset = Teacher.objects.all().only('name', 'good_count', 'bad_count')
#     names = [teacher.name for teacher in queryset]
#     good_counts = [teacher.good_count for teacher in queryset]
#     bad_counts = [teacher.bad_count for teacher in queryset]
#     return JsonResponse({'names': names, 'good': good_counts, 'bad': bad_counts})
