import os
import random
from celery.result import AsyncResult
from football_platform.celery import app
from django.contrib.auth.mixins import LoginRequiredMixin
from tool.send_notices import SendNotices
from IPython.core.display import JSON
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.views.generic import ListView
from football_platform import settings
from .models import NewUser,Notification
from rest_framework import viewsets,status
from rest_framework.response import Response
from user.serializers import UserSerializer,UpdateUserSerializer,NotificationSerializer
from football_platform.settings import BASE_URL
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer
from django.core.cache import cache
from django.views.decorators.cache import cache_page #在视图函数中使用,将视图结果存入缓存
import json
from tool.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms_c,mongo_insert
from notifications.signals import notify
from django.contrib.auth.hashers import check_password
# Create your views here.

MEDIA_ADDR = '/media/'
Position = [ '中锋', '边锋', '前腰', '后腰', '中前卫', '左前卫', '右前卫', '中后卫', '左后卫', '右后卫', '门将']
Sex = ['女','男']


#进行路径拼接
def get_avatar_url(avatar):
    '''返回头像的url'''
    if avatar == 'default.jpg':
        return MEDIA_ADDR + 'avatar/' + str(avatar)
    else:
        return MEDIA_ADDR + str(avatar)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

#获取登录用户信息
class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']
   # @cache_page(300)  # 5分钟
    def list(self, request, *args, **kwargs):
        print('ok')
        print(request.user.id)
        user_info = NewUser.objects.get(id=request.user.id)
        roles = request.user.roles
        print(roles)
        if roles == 1:
            #print(type(request.user))
            #print(type(user_info))
            avatar = request.user.avatar
            position = int(user_info.position)
            sex = int(user_info.sex)
            #user_info.avatar = str(get_avatar_url(avatar))
            #print(type(user_info.avatar))
            user_info.position = Position[position]
            user_info.sex = Sex[sex]
            #notice = SendNotices()
            #notice.send(request.user,request.user,'通知')  # 发送消息
            #unread_list = notice.get_unread_list(request.user) #未读列表

            #print(str(unread_list))
        try:
            notices = Notification.objects.get(verb='平台用户通知')
        except Exception as e:
            print(request)
            user = NewUser.objects.get(id=16)
            notify.send(sender=user,recipient=request.user,verb='平台用户通知',target=None,description='尊敬的用户:\r\n   欢迎您使用足球训练分析平台')

        if roles == 0:
            user_info.roles = 'admin'
        elif roles == 1:
            user_info.roles = 'user'
        else:
            user_info.roles = 'coach'

        serializer = UserSerializer(instance=user_info, many=False)
        print(serializer.data)
        return Response(serializer.data)
        #return Response(user_info)

#获取所有用户信息
#@cache_page(300) #5分钟
class UserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer



class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
    permission_classes = []


    def create(self, request, *args, **kwargs):
        #get_serializer:获取序列化对象
        serializer = self.get_serializer(data=request.data)#在内部实现了get_serializer_class()(获取序列化类)
        #或者:serialzer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = request.data['code']
        phone = request.data['phone']
        old_code = cache.get('sms_%s'%(phone))
        if not old_code:

            return Response({'status':'404'})

        if int(code) != old_code:
            return Response({'status': '404'})
        user_info = self.perform_create(serializer)
        user_info.set_password(request.data['password'])
        user_info.is_active = True #刚开始注册的用户未被激活
        user_info.save()
        #url = request.build_absolute_uri("/api/user_activate/" + str(code) + "/")
        #url = BASE_URL + "/api/user_activate/" + str(code)
        #print(url)

        #发送邮件给用户激活
        #send_mail('用户激活', url,'15016299762@163.com',[user_info.email],fail_silently=False)
        #检查验证码是否正确
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class UploadAvatarView(APIView):

    def post(self, request):
       file = request.data.get('file')
       uid = request.data.get('id')
       user_obj = NewUser.objects.get(id=uid)
       user_obj.avatar = 'avatar/' + file.name
       user_obj.save()
       media_path = "media/avatar"
       file_path = os.path.join(settings.BASE_DIR, media_path)
       file_name = os.path.join(file_path, file.name)
       # wb  以二进制形式写入
       with open(file_name, "wb") as f:
           # 写入字节流
           f.write(file.file.read())
           print(file.file.read())
           print(type(file))
           # 返回响应
           data = {
               "code": 200,
               'msg': "上传图片成功",
               'media_path': media_path,
           }
           return Response(data)



class UploadFilesView(APIView):
    def post(self,request):
        file = request.data.get('file')
        id = request.user.id
        member_anal=mongo_insert.delay(str(file.file.read()),id)
        async_task = AsyncResult(id=member_anal.id,app=app)
        print(async_task.get())
        print(1111)
        data = {
            "code": 200,
            'msg': "上传文件成功",
            'member_anal':async_task.get()
        }
        return Response(data)



class UserUpdateViewSet(GenericAPIView):
    queryset = NewUser.objects.all()
    serializer_class = UpdateUserSerializer
    http_method_names = ['put']

    def put(self, request, id):
        print(request.data)
        user_obj = NewUser.objects.get(id=id)
        if request.data['flag'] == 0:
            for i in range(9):
                if Position[i] == request.data['position']:
                    request.data['position'] = str(i)
                    break
        if request.data['flag'] == 2:
            oldpass = request.data['password']
            print(check_password(oldpass,user_obj.password))
            if check_password(oldpass,user_obj.password):
                print(999999)
                user_obj.set_password(request.data['newpass'])
                user_obj.save()
        validated_data = UpdateUserSerializer(data=request.data, instance=user_obj) #反序列化
        if validated_data.is_valid():
            validated_data.save()  #返回数据对象实例
            return Response(validated_data.data)
        else:
            return Response(validated_data.errors)

#获取个人信息
class UserInfo(APIView):
    def get(self,request,username):
        print('000')
        user_info = NewUser.objects.get(username=username)
        if user_info.roles == 'coach':
            data = {
                'code':200,
                'msg':'请输入球员姓名',
            }
            return Response(data)
        print(type(user_info))
        position = int(user_info.position)
        sex = int(user_info.sex)
        avatar = user_info.avatar
        print(avatar)
        #user_info.avatar = get_avatar_url(avatar)
        user_info.position = Position[position]
        user_info.sex = Sex[sex]
        print(user_info.avatar)
        serializer = UserSerializer(instance=user_info, many=False)
        return Response(serializer.data)

class NoticeView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    http_method_names = ['get','put','delete']

    # 未读通知的查询集
    def get(self,request):
        #返回用户未读列表
        notices = Notification.objects.filter(recipient=request.user.id)
        serializer = self.get_serializer(instance=notices,many=True)

        for data in serializer.data:
            id = data['actor_object_id']
            user = NewUser.objects.get(id=id)
            data['actor'] = user.username
        print(serializer.data)
        return Response(serializer.data)

    def put(self,request,id):
        notice = Notification.objects.get(id=id)
        serializer = self.get_serializer(instance=notice, data=request.data)
        if serializer.is_valid():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

    def delete(self,request,id):
        try:
            Notification.objects.get(id=id).delete()
        except Exception as e:
            print(e)
        data = {
            "status": 200,
            'msg': "删除文件成功",
        }
        return Response(data)





#发送短信获取验证码
class Sms(APIView):
    http_method_names = ['post']
    permission_classes = [] #不需要权限和认证就可以执行

    def post(self,request):
        phone = request.data['phone']
        #生成验证码
        code = random.randint(1000,9999)
        #存储验证码 django-redis
        cache_key = 'sms_%s'%(phone)
        #检查是否有已发过的且未过期的验证码
        old_code = cache.get(cache_key)
        if old_code:
            return Response({'status':'404'})
        cache.set(cache_key,code,60) #60秒有效
        #发送验证码
        #send_sms(phone,code)
        #celery版
        send_sms_c.delay(phone,code) #启动celery(celery -A football_platform worker -l info) #推送到redis的队列里
        return Response('')


def send_sms(phone,code):
    config = {
        "accountSid": settings.ACCOUNTSID,
        "accountToken": settings.ACCOUNTTOKEN,
        "appId": settings.APPID,
        "templateId": '1',
    }
    yun = YunTongXin(**config)  # 变为关键字传参
    res = yun.run(phone, code)
    return res



