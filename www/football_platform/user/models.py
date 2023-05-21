from datetime import datetime
import six
from django.db import models
from django.contrib.auth.models import AbstractUser #用户模型类
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
#使用AbstractUser可以对User进行扩展使用
class NewUser(AbstractUser):

    role_type = [
        [0, 'admin'],
        [1, 'user'],
        [2, 'coach'],
    ]

    Sex = [
        ['0', '女'],
        ['1', '男'],
    ]

    Position = [
        ['0', '中锋'],
        ['1', '边锋'],
        ['2', '前腰'],
        ['3', '后腰'],
        ['4', '中前卫'],
        ['5', '左前卫'],
        ['6', '右前卫'],
        ['7', '中后卫'],
        ['8', '左后卫'],
        ['9', '右后卫'],
        ['10', '门将'],
    ]

    roles = models.IntegerField(verbose_name='角色', choices=role_type, default=1)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, auto_now=True)
    #code = models.UUIDField(verbose_name='uuid', default=uuid.uuid4, editable=False) #唯一的,不会重复,通识唯一识别码
    avatar = models.ImageField(verbose_name='头像',default='default.jpg', upload_to='avatar')
    age = models.IntegerField(verbose_name='年龄', null=True)
    phone = models.CharField(verbose_name='手机号',max_length=11)
    sex = models.CharField(verbose_name='性别', choices=Sex, null=True,max_length=32)
    weight = models.FloatField(verbose_name='体重', null=True)
    stature = models.FloatField(verbose_name='身高',null=True)
    position = models.CharField(verbose_name='位置',choices=Position, null=True,max_length=32)
    pass_football = models.FloatField(verbose_name='传球',default=0)
    hotshot = models.FloatField(verbose_name='射门',default=0)
    speed_num = models.FloatField(verbose_name='加速次数',default=0)
    join_time = models.FloatField(verbose_name='上场时长(分钟)',default=0)
    sprint_distance = models.FloatField(verbose_name='冲刺距离(公里)',default=0)
    sprint_num = models.FloatField(verbose_name='冲刺次数',default=0)
    heart_avg = models.FloatField(verbose_name='平均心率',default=70)
    run_distance = models.FloatField(verbose_name='跑动距离(公里)',default=0)
    football_tream = models.CharField(verbose_name='球队',max_length=64, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间',default=datetime.now)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        db_table = 'NewUser'
        swappable = 'AUTH_USER_MODEL'
        pass

    def __str__(self): #在管理后台显示
        return self.username


from notifications.base.models import AbstractNotification


class Notification(AbstractNotification):

    class Meta(AbstractNotification.Meta):
        abstract = False
        verbose_name_plural = '通知'

