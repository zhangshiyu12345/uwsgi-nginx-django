#中间件
from django.utils.deprecation import MiddlewareMixin


class UserMiddleware(MiddlewareMixin):

    def process_request(self,request):
        print('UserMiddleware')

    def process_view(self,request,callback,callback_args,callback_kwargs):
        print('UserMiddleware process_view')

    def process_response(self,request,response):
        print('UserMiddleware process_response')

        return response  #返回视图函数里的response