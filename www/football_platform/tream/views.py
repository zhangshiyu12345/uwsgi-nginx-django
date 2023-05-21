from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import Match,FootballTream
from tream.serializers import MatchSerializers,FootballTreamSerialzers
import csv
import os
from django.conf import settings
from .tasks import csv_pre,pass_count,player_anal
from football_platform.celery import app

class MatchView(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('-match_id')
    serializer_class = MatchSerializers

class TreamViewSet(viewsets.ModelViewSet):
    queryset = FootballTream.objects.all()
    serializer_class = FootballTreamSerialzers


class TreamInfo(APIView):
    def get(self,requst,football_tream):
        tream_obj = FootballTream.objects.get(name=football_tream)
        serializer = FootballTreamSerialzers(instance=tream_obj,many=False)
        return Response(serializer.data)

class TreamCreateViewSet(GenericViewSet):
    queryset = FootballTream.objects.all()
    serializer_class = FootballTream
    permission_classes = []

    def create(self, request):
        bs = FootballTreamSerialzers(data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)



class MatchDetailView(APIView):
    def get(self,request,match_id):
        match = Match.objects.get(match_id=match_id)
        media_path = "media/files"
        file_path = os.path.join(settings.BASE_DIR, media_path)
        treams_member_dict = csv_pre.delay(file_path)
        serializer = MatchSerializers(instance=match)

        async_task = AsyncResult(id=treams_member_dict.id,app=app)
        print(async_task.get())

        graph = pass_count.delay(file_path)
        async_task_graph = AsyncResult(id=graph.id,app=app)


        data1 = {
            'data':serializer.data,
            'treams_member_dict':async_task.get(),
            'graph':async_task_graph.get(),
        }
        return Response(data1)

class PlayerDetailView(APIView):
    def get(self,request,match_id):
        media_path = "media/players"
        file_path = os.path.join(settings.BASE_DIR, media_path)
        player_analy = player_anal.delay(file_path)
        async_task = AsyncResult(id=player_analy.id, app=app)
        print(async_task.get())

        data = {
            'player_traject':async_task.get()
        }

        return Response(data)

class UploadTreamView(APIView):
    def post(self,request):
        file = request.data.get('file')
        media_path = "media/files"
        file_path = os.path.join(settings.BASE_DIR,media_path)
        file_name = os.path.join(file_path, file.name)
        print(file.name)
        with open(file_name,"wb") as f:
            f.write(file.file.read())
            data = {
                "code":200,
                'msg':'上传团队文件成功',
                'media_path':media_path,
            }
            return Response(data)

class UploadPlayerView(APIView):
    def post(self,request):
        file = request.data.get('file')
        media_path = "media/players"
        file_path = os.path.join(settings.BASE_DIR, media_path)
        file_name = os.path.join(file_path, file.name)
        print(file.name)
        with open(file_name, "wb") as f:
            f.write(file.file.read())
            data = {
                "code": 200,
                'msg': '上传团队文件成功',
                'media_path': media_path,
            }
            return Response(data)

class UploadEmblemView(APIView):
    def post(self,request):
        file = request.data.get('file')
        football_tream = request.user.football_tream
        tream_obj = FootballTream.objects.get(name=football_tream)
        print(file)
        print(file.file)
        tream_obj.tream_emblem = file
        tream_obj.save()
        media_path = "media/tream"
        file_path = os.path.join(settings.BASE_DIR, media_path)
        file_name = os.path.join(file_path, file.name)
        # wb  以二进制形式写入
        with open(file_name, "wb") as f:
            # 写入字节流
            for chunk in file.chunks():
                f.write(chunk)
            print(file.file.read())
            print(type(file))
            # 返回响应
            data = {
                "code": 200,
                'msg': "上传图片成功",
                'media_path': media_path,
            }
            return Response(data)