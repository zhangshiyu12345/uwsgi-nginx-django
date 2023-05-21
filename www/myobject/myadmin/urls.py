#后台管理子路由文件
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
     path('',views.index1,name="myadmin_index"),#后台首页

     #后台管理员登录，退出路由
     path('login',views.login,name="myadmin_login"),#加载登录表单
     path('dologin',views.dologin,name="myadmin_dologin"),#执行登录
     path('logout',views.logout,name="myadmin_logout"),#退出
     path('verify',views.verify,name="myadmin_verify"),#输出验证码

     #员工信息管理路由
     path('user/<int:pIndex>',views.index,name="myadmin_user_index"), #name用于模板层反向解析路经
     path('user/add',views.add,name="myadmin_user_add"),#添加表单
     path('user/insert',views.insert,name="myadmin_user_insert"),#执行添加
     path('user/delete/<int:uid>',views.delete,name="myadmin_user_delete"),#执行删除
     path('user/edit/<int:uid>',views.edit,name="myadmin_user_edit"),#加载编辑表单
     path('user/update/<int:uid>',views.update,name="myadmin_user_update"),#执行编辑

     #店铺信息管理路由
     path('shop/<int:pIndex>',views.shop_index,name="myadmin_shop_index"), #name用于模板层反向解析路经
     path('shop/add',views.shop_add,name="myadmin_shop_add"),#添加表单
     path('shop/insert',views.shop_insert,name="myadmin_shop_insert"),#执行添加
     path('shop/delete/<int:sid>',views.shop_delete,name="myadmin_shop_delete"),#执行删除
     path('shop/edit/<int:sid>',views.shop_edit,name="myadmin_shop_edit"),#加载编辑表单
     path('shop/update/<int:sid>',views.shop_update,name="myadmin_shop_update"),#

     # 菜品类别信息管理路由
     path('category/<int:pIndex>', views.category_index, name="myadmin_category_index"),  # name用于模板层反向解析路经
     path('category/load/<int:sid>',views.category_loadCategory,name="myadmin_category_load"),
     path('category/add', views.category_add, name="myadmin_category_add"),  # 添加表单
     path('category/insert', views.category_insert, name="myadmin_category_insert"),  # 执行添加
     path('category/delete/<int:cid>', views.category_delete, name="myadmin_category_delete"),  # 执行删除
     path('category/edit/<int:cid>', views.category_edit, name="myadmin_category_edit"),  # 加载编辑表单
     path('category/update/<int:cid>', views.category_update, name="myadmin_category_update"),# 执行编辑

     # 菜品信息管理路由
     path('product/<int:pIndex>', views.product_index, name="myadmin_product_index"),  # name用于模板层反向解析路经
     path('product/add', views.product_add, name="myadmin_product_add"),  # 添加表单
     path('product/insert', views.product_insert, name="myadmin_product_insert"),  # 执行添加
     path('product/delete/<int:pid>', views.product_delete, name="myadmin_product_delete"),  # 执行删除
     path('product/edit/<int:pid>', views.product_edit, name="myadmin_product_edit"),  # 加载编辑表单
     path('product/update/<int:pid>', views.product_update, name="myadmin_product_update"),  # 执行编辑

     #会员信息管理路由
     path('member/<int:pIndex>',views.member_index,name="myadmin_member_index"),
]