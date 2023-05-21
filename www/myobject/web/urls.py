#前台大堂点餐
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('',views.index,name="web_index"),

   #前台登录推出的路由
   path('login',views.login,name="web_login"),
   path('dologin',views.dologin,name="web_dologin"),
   path('logout',views.logout,name="web_logout"),
   path('verify',views.verify,name="web_verify"),

   #为url路由添加请求前缀web/,凡是带此前缀的url地址必须登录后才可访问
   path("web/",include([
      path('',views.webindex,name="web_index"),#前台大堂点餐首页
      #购物车信息管理路由
      path('cart/add/<str:pid>',views.cart_add,name="web_cart_add"),
      path('cart/delete/<str:pid>',views.cart_delete,name="web_cart_delete"),
      path('cart/change',views.cart_change,name="web_cart_change"),
      path('cart/clear',views.cart_clear,name="web_cart_clear"),

   #订单处理路由
      path('order/<int:pIndex>',views.order_index,name="web_orders_index"),#订单浏览
      path('order/insert',views.order_insert,name="web_orders_insert"),#执行订单添加功能
      path('order/detail', views.order_detail, name="web_orders_detail"),#订单祥情
      path('order/status', views.order_status, name="web_orders_status"),  # 订单状态修改
   ]))
]