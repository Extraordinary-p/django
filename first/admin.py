from django.contrib import admin
from django.contrib.auth.models import User

from first.models import *

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'intro', 'is_hot') #将这些字段都展示出来
    search_fields = ('name', ) #支持搜索框的字段
    ordering = ('no', ) #按照no字段进行排序
    list_editable = ('is_hot',) #列表页直接编辑


class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'sex', 'birth')
    search_fields = ('name', )
    ordering = ('no', )

admin.site.register(Subject, SubjectModelAdmin)
admin.site.register(Teacher,TeacherModelAdmin)
# Register your models here.
