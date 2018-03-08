import xadmin

from .models import Course, Lesson, Video, CourseRescource

class LessonInline(object):
    model = Lesson
    extra = 0


class VideoInline(object):
    model = Video
    extra = 0


class CourseXadmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'student_nums', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'degree']
    list_filter = ['name', 'degree' , 'learn_times', 'student_nums', 'fav_nums', 'click_nums', 'add_time']
    list_editable = ['name', 'desc', 'degree', 'learn_times']
    readonly_fields = ['student_nums', 'fav_nums', 'click_nums', 'add_time']
    show_detail_fields = ['name']
    model_icon = 'fa fa-star'
    inlines = [LessonInline]


class LessonXadmin(object):
    list_display = ['course', 'name' ,'add_time']
    search_fields = ['name']
    list_filter = ['add_time']
    list_editable = ['course', 'name']
    readonly_fields = ['add_time']
    model_icon = 'fa fa-tachometer'
    inlines = [VideoInline]


class VideoXadmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['name']
    list_filter = ['add_time']
    list_editable = ['lesson', 'name']
    readonly_fields = ['add_time']
    model_icon = 'fa fa-caret-square-o-right'


class CourseRescourceXadmin(object):
    list_display = ['course', 'name', 'url']
    search_fields = ['name']
    list_editable = ['course', 'name', 'url']
    model_icon = 'fa fa-random'


xadmin.site.register(Course, CourseXadmin)
xadmin.site.register(Lesson, LessonXadmin)
xadmin.site.register(Video, VideoXadmin)
xadmin.site.register(CourseRescource, CourseRescourceXadmin)