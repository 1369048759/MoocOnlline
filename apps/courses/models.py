from django.db import models

from datetime import datetime

from organization.models import CourseOrg, Teacher
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50, default=u'', verbose_name=u'课程名称')
    image = models.ImageField(max_length=100, upload_to='course/%Y%m', verbose_name=u'课程图片')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(max_length=2, choices=(('cj','初级'),('zj','中级'),('gj','高级')), verbose_name=u'课程难度')
    org = models.ForeignKey(CourseOrg, null=True, blank=True, verbose_name=u'所属机构')
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name=u'授课讲师')
    category = models.CharField(max_length=50, default=u'后端开发', verbose_name=u'课程类别')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    student_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    course_info = models.CharField(max_length=300, default=u'', verbose_name=u'课程须知')
    knowledge_info = models.CharField(max_length=300, default=u'', verbose_name=u'课程知识')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')

    class Meta:
        verbose_name = u'课程信息'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_lesson(self):
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_video(self):
        return self.video_set.all()

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=200, default=u'', verbose_name=u'视频地址')
    image = models.ImageField(max_length=100, upload_to='course/video/%Y%m', default=u'course/video/default.png', verbose_name=u'视频封面')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseRescource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'文件名称')
    url = models.FileField(max_length=100, upload_to='course/rescource/%Y%m', verbose_name=u'文件路径')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

