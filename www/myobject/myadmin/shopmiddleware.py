#自定义中间件类(执行是否登录判断)
#登录一定要在后台的外边
from django.shortcuts import redirect
from django.urls import reverse
import re
class ShopMiddleware:
    def __init__(self, get_response):#（启动时会被掉用一次）
        self.get_response = get_response
        # One-time configuration and initialization.
        print("ShopMiddleware")

    def __call__(self, request):
        path=request.path
        print("url:",path)

        #判断管理后台是否登录
        #定义后台不登录也可以直接访问的url列表
        urllist=['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
        #判断当前请求url地址是否是以/myadmin开头,并且不在urllist中,才做是否登录判断
        if re.match(r'^/myadmin',path) and (path not in urllist):
            #判断是否登录
            if 'adminuser' not in request.session:
            #(重定向到登录页)
                return redirect(reverse('myadmin_login'))

        #判断大堂点餐请求的判断，判断是否登录(判断session中是否有webuser)
        if re.match(r'^/web', path):
            # 判断是否登录
            if 'webuser' not in request.session:
                # (重定向到登录页)
                return redirect(reverse('web_login'))

        #判断移动端是否登录
        urllist = ['/mobile/register', '/mobile/doregister']
        # 判断当前请求url地址是否是以/myadmin开头,并且不在urllist中,才做是否登录判断
        if re.match(r'^/mobile', path) and (path not in urllist):
            # 判断是否登录
            if 'mobileuser' not in request.session:
                # (重定向到登录页)
                return redirect(reverse('mobile_register'))

        response = self.get_response(request)



        return response
#在setting.py中的配置被实例化,每一次的请求都会经过
#由于是在setting.py中被注册了，所以整个项目都会路过这个中间件