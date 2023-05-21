"""football_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from user.views import UserViewSet, UserCreateViewSet, MyObtainTokenPairView, UserInfoViewSet, UploadAvatarView,UserUpdateViewSet,UserInfo,Sms,UploadFilesView,NoticeView
from tream.views import MatchView,MatchDetailView,UploadTreamView,TreamCreateViewSet,UploadEmblemView,TreamInfo,TreamViewSet,UploadPlayerView,PlayerDetailView
import notifications.urls
from django.views.generic import TemplateView
# 导入 simplejwt 提供的几个验证视图类
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
router_V1 = routers.DefaultRouter()
router_V1.register('info', UserInfoViewSet)
router_V1.register('user_activate', UserCreateViewSet)
router_V1.register('users_create',UserCreateViewSet)
router_V1.register(r'users',UserViewSet)
router_V1.register(r'treams',TreamViewSet)
router_V1.register(r'match',MatchView)
router_V1.register(r'tream_create',TreamCreateViewSet)


urlpatterns = [
    path('',TemplateView.as_view(template_name="index.html")),
    path('api/', include(router_V1.urls)),
    path('admin/', admin.site.urls),
    #path('xadmin/',xadmin.site.urls),
    # 获取Token的接口
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token有效期的接口
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/avatar/', UploadAvatarView.as_view(), name='upload_avatar'),
    path('api/files/', UploadFilesView.as_view(), name='upload_files'),
    path('api/user_update/<int:id>/', UserUpdateViewSet.as_view(), name="user_update"),
    path('api/userinfo/<str:username>/', UserInfo.as_view()),
    path('api/sms/',Sms.as_view(),name='sms_phone'),
    path('inbox/notifications/',include(notifications.urls,namespace='notifications')),
    path('api/notice/',NoticeView.as_view(),name='notice'),
    path('api/notice/<int:id>/',NoticeView.as_view(),name='update_notice'),
    path('api/notice/delete/<int:id>/',NoticeView.as_view(),name='delete_notice'),
    path("api/match_data/<int:match_id>/", MatchDetailView.as_view(),name='match_detail_data'),
    path("api/player_data/<int:match_id>/", PlayerDetailView.as_view(),name='player_detail_data'),
    path("api/tream/files",UploadTreamView.as_view(),name='upload_tream_files'),
    path("api/tream_emblem/",UploadEmblemView.as_view(),name='upload_tream_emblem'),
    path("api/treaminfo/<str:football_tream>/",TreamInfo.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
