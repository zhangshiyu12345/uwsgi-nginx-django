from django.urls import path, include
from .models import NewUser,Notification
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Serializers define the API representation.
from notifications.signals import notify

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'

    def create(self,validated_data):
        #** 对validated_data进行拆包操作
        res = NewUser.objects.create(**validated_data)
        return res



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['weight'] = user.weight
        token['sex'] = user.sex
        token['age'] = user.age
        token['position'] = user.position
        token['stature'] = user.stature
        token['phone'] = user.phone

        return token

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['username', 'weight', 'stature', 'age', 'position','phone','football_tream','password']


class NotificationSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'