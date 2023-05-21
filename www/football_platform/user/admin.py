from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import NewUser

# Register your models here.

class NewUserAdmin(UserAdmin):

    #做表格切割(字段集标题,字段集信息)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name', 'sex', 'age', 'weight', 'stature', 'position', 'avatar', 'join_time', 'football_tream', 'speed_num', 'heart_avg', 'sprint_num', 'sprint_distance', 'hotshot', 'run_distance', 'phone','pass_football')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'roles')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )

    list_display = ('id', 'username', 'roles', 'email', 'phone', 'age', 'sex', 'weight', 'stature', 'position', 'football_tream', 'join_time', 'pass_football', 'run_distance', 'sprint_distance', 'hotshot', 'speed_num','is_active', 'create_time', 'last_login')
    list_display_links = ('id', 'username', 'roles', 'email', 'football_tream', 'pass_football', 'sprint_distance', 'hotshot', 'last_login') #跳转到修改页
    search_fields = ('username', 'email', 'sex', 'age', 'position', 'football_tream', 'roles',) #搜索框的提示文字

admin.site.register(NewUser, NewUserAdmin)


#class NoticeAdmin(admin.ModelAdmin):
    #list_display = ('id', 'title', 'author')
    #list_display_links = ('id', 'title') #要在list_display中出现
    #search_fields = ('title',)

#admin.site.register(Notice, NoticeAdmin)

