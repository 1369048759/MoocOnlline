from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50, default=u'', verbose_name=u'城市名称')
    desc = models.CharField(max_length=200, verbose_name=u'城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    image = models.ImageField(max_length=100, upload_to='org/%Y%m', verbose_name=u'机构图片')
    category = models.CharField(max_length=10, choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')), default='pxjg', verbose_name=u'机构类别')
    desc = models.CharField(max_length=200, verbose_name=u'机构描述')
    detail = UEditorField(
        width=800, height=600, imagePath="/org/",
        filePath="/org/", verbose_name=u"机构详情"
    )
    classis_course = models.CharField(max_length=50, default='', verbose_name=u'经典课程')
    city = models.ForeignKey(City, verbose_name=u'所在城市')
    address = models.CharField(max_length=200, verbose_name=u'机构地址')
    student_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_course_nums(self):
        return self.course_set.all().count()


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    age =  models.IntegerField(default=0, verbose_name=u'年龄')
    image = models.ImageField(max_length=100, upload_to='teacher/%Y%m', verbose_name=u'头像')
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    point = models.CharField(max_length=50, verbose_name=u'教学特点')
    blog = models.CharField(max_length=200, default=u'', verbose_name=u'博客')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'讲师信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()


class OrgImage(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    image = models.ImageField(max_length=100, upload_to='orgImage/%Y%m', verbose_name=u'头像')
    index = models.IntegerField(default=1, verbose_name=u'序号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'机构图片'
        verbose_name_plural = verbose_name


