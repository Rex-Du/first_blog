#!/usr/bin/env python
# coding    :   utf-8
# Author    :   DQ
# CreatTime :   2017-06-07 15:12
from io import BytesIO
from blog.utils.check_code import create_validate_code
from django.shortcuts import HttpResponse
import json
from django import forms
from django.forms import widgets
from blog.models import *
from django.shortcuts import render, redirect


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    # stream = BytesIO()
    # img, code = create_validate_code()
    # img.save(stream, 'PNG')
    # request.session['CheckCode'] = code
    # return HttpResponse(stream.getvalue())

    # data = open('static/imgs/avatar/20130809170025.png','rb').read()
    # return HttpResponse(data)

    # 1. 创建一张图片 pip3 install Pillow
    # 2. 在图片中写入随机字符串
    # obj = object()
    # 3. 将图片写入到制定文件
    # 4. 打开制定目录文件，读取内容
    # 5. HttpResponse(data)

    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        label='用户名',
        required=True,
        error_messages={'required': '不能为空'}
    )
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}), label='密码', min_length=1)


def login(request, *args):
    try:
        if request.method == 'GET':
            obj = UserLoginForm()

        if request.method == 'POST':
            obj = UserLoginForm(request.POST)
            if obj.is_valid():
                user = obj.cleaned_data['username']
                passwd = obj.cleaned_data['password']

                user_exists = User.objects.filter(username=user).count()
                if user_exists:
                    user_info = User.objects.get(username=user)
                    if user_info.password == passwd:
                        res = redirect('/index')
                        request.session['username'] = user
                        request.session['islogin'] = True

                        code = request.POST['code'].lower()
                        if code == request.session['CheckCode'].lower():
                            statu = 1
                        else:
                            statu = 0
                        data = {'hehe': statu}
                        return res
                    else:
                        response = HttpResponse()
                        response.write('<script>alert("用户名或密码错误");window.location=window.location</script>')
                        return response
                else:
                    response = HttpResponse()
                    response.write('<script>alert("用户名或密码错误");window.location=window.location</script>')
                    return response
            else:
                response = HttpResponse()
                response.write('<script>alert("用户名或密码错误格式错误");window.location=window.location</script>')
                return response
    except Exception as e:
        print(e)
    return render(request, 'login.html', locals())  # 返回登录页面
