import xadmin

from .models import City, CourseOrg, Teacher, OrgImage

class CityXadmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    list_editable = ['name', 'desc']
    readonly_fields = ['add_time']
    model_icon = 'fa fa-sitemap'


class CourseOrgXadmin(object):
    list_display = ['name', 'desc', 'classis_course', 'city', 'address', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'city', 'address']
    list_filter = ['name', 'desc', 'city', 'address', 'fav_nums', 'click_nums', 'add_time']
    list_editable = ['name', 'desc', 'classis_course',  'city', 'address']
    readonly_fields = ['fav_nums', 'click_nums', 'add_time']
    show_detail_fields = ['name']
    model_icon = 'fa fa-globe'


class TeacherXadmin(object):
    list_display = ['name', 'age', 'org', 'work_company', 'work_position', 'work_years', 'point', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'org', 'work_company', 'work_position', 'point']
    list_filter = ['name', 'age', 'org', 'work_company', 'work_position', 'work_years', 'point', 'fav_nums', 'click_nums', 'add_time']
    list_editable = ['name', 'age', 'org', 'work_company', 'work_position', 'work_years', 'point']
    readonly_fields = ['fav_nums', 'click_nums', 'add_time']
    show_detail_fields = ['name']
    model_icon = 'fa fa-female'


class OrgImageXadmin(object):
    list_display = ['org', 'image', 'index', 'add_time']
    search_fields = ['org', 'org', 'work_company', 'work_position', 'point']

    model_icon = 'fa fa-female'


xadmin.site.register(City, CityXadmin)
xadmin.site.register(CourseOrg, CourseOrgXadmin)
xadmin.site.register(Teacher, TeacherXadmin)
xadmin.site.register(OrgImage, OrgImageXadmin)