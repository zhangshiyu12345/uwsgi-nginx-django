from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'football_platform.settings')
app = Celery('football_platform',backend='redis://:245478@175.178.248.34:6379/0') #celery初始化,名字为football_platform
app.conf.update(
    broker_url = 'redis://:245478@175.178.248.34:6379/1',
)

#自动去应用下找worker函数
app.autodiscover_tasks(settings.INSTALLED_APPS)
