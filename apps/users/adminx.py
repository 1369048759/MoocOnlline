import xadmin
from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Banner

class UserProfileXadmin(object):
    pass


class EmailVerifyRecordXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'add_time']
    model_icon = 'fa fa-folder-open'


class BannerXadmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title']
    list_filter = ['title', 'add_time']
    list_editable = ['title', 'iamge', 'url', 'index']
    model_icon = 'fa fa-fire'

#添加主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


#修改页头页尾
class GlobalSettings(object):
    site_title = 'MOOC Admin'
    site_footer = 'MOOC Online'
    menu_style = 'accordion'

#xadmin.site.register(UserProfile, UserProfileXadmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordXadmin)
xadmin.site.register(Banner, BannerXadmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)