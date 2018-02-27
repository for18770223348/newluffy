from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import views
import pymysql
from luffy_backend import settings
from api import models
import json
import hashlib
import time


class LoginView(views.APIView):
    authentication_classes = []
    def get(self,request,*args,**kwargs):
        ret = {
            'code':1000,
            'data':'老男孩'
        }
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def post(self,request,*args,**kwargs):
        ret = {
            'code':1000,
            'username':'',
            'token':''

        }
        body=request.body
        read_body=json.loads(body)

        user_obj = models.Account.objects.filter(**read_body).first()

        if user_obj:
            print(user_obj)
            ret['username']=user_obj.username

            ret['token']=user_obj.userauthtoken.token

        else:
            ret['code']=404
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def options(self, request, *args, **kwargs):
        # self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        # self.set_header('Access-Control-Allow-Headers', "k1,k2")
        # self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        # self.set_header('Access-Control-Max-Age', 10)

        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        # response['Access-Control-Allow-Methods'] = 'PUT'
        return response

class RegiestView(views.APIView):
    authentication_classes = []

    def get(self,request,*args,**kwargs):
        pass

    def post(self,request,*args,**kwargs):
        ret={
            'code':1001,
            'msg':''
        }
        body=request.body
        body1=json.loads(body)
        body1.pop('nextpassword')
        user_obj=models.Account.objects.filter(username=body1.get('username'))
        if not user_obj:
            user = models.Account.objects.create(**body1)
            m=hashlib.md5()
            m.update(str(time.time()).encode(encoding='utf-8'))
            models.UserAuthToken.objects.create(user=user,token=m.hexdigest())
        else:
            ret={'code':404,'msg':'该用户已经注册'}

        response=JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def options(self, request, *args, **kwargs):
        # self.set_header('Access-Control-Allow-Origin', "http://www.xxx.com")
        # self.set_header('Access-Control-Allow-Headers', "k1,k2")
        # self.set_header('Access-Control-Allow-Methods', "PUT,DELETE")
        # self.set_header('Access-Control-Max-Age', 10)

        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        # response['Access-Control-Allow-Methods'] = 'PUT'
        return response

