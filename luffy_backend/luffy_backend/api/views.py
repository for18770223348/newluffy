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
        print(user_obj)
        if user_obj:
            ret['username']=user_obj.username
            userauthtoken_obj=models.UserAuthToken.objects.filter(user=user_obj).first()
            ret['token']=userauthtoken_obj.token

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