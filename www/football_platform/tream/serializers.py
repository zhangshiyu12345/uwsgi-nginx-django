from .models import Match,FootballTream
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class FootballTreamSerialzers(serializers.ModelSerializer):
    class Meta:
        model = FootballTream
        fields = '__all__'
