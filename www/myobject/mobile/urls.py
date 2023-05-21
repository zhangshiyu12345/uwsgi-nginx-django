from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index,name="mobile_index"),#移动端首页
    #会员注册/登录
    path('register',views.register,name="mobile_register"),
    path('doregister',views.doRegister,name="mobile_doregister"),
    #店铺选择
    path('shop',views.shop,name="mobile_shop"),#店铺选择
    path('shop/select',views.selectShop,name="mobile_selectshop"),#执行移动端店铺选择
    #购物车信息管理路由
    path('cart/add', views.cart_add, name="mobile_cart_add"),
    path('cart/delete', views.cart_delete, name="mobile_cart_delete"),
    path('cart/change', views.cart_change, name="mobile_cart_change"),
    path('cart/clear', views.cart_clear, name="mobile_cart_clear"),
    #订单处理
    path('orders/add',views.addOrders,name="mobile_addorders"),#加载移动端订单页
    path('orders/doadd',views.doAddOrders,name="mobile_doaddorders"),#执行移动端订单添加操作
    #会员中心
    path('member',views.member_index,name="mobile_member_index"),#会员中心首页
    path('member/orders',views.member_orders,name="mobile_member_orders"),#加载会员中心订单页
    path('member/detail',views.member_detail,name="mobile_member_detail"),#加载会员订单祥情页
    path('member/logout',views.member_logout,name="mobile_member_logout"),#执行退出

]