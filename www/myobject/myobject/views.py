from django.shortcuts import render
from django.http import HttpResponse
import time
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
import csv

def index(request):
    return HttpResponse("欢迎进入点餐系统的后台管理")
