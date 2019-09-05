# coding:utf-8
from django.shortcuts import render, redirect
import logging
from blog.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.forms import widgets
import datetime
import json
import os
from django.conf import settings
# Create your views here.


class UserInfoModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'qq', 'mobile']
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '用户名'}),
            'password': forms.PasswordInput,
            'email': forms.EmailInput,
        }

loger = logging.getLogger('blog.views')


def global_setting(request, *args):
    # 分类信息获取
    category_list = Category.objects.all()
    # 广告数据（自己完成）
    ad_list = Ad.objects.all()
    # 文章排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('comment_count')
    article_order_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    # 文章归档
    tar_list = Article.objects.date_format()
    # return {
    #     'SITE_NAME':settings.SITE_NAME,
    #     'SITE_DESC':settings.SITE_DESC,
    #     'category_list':category_list,
    #     'ad_list':ad_list,
    #     'guidan_list':guidan_list,
    # }
    # 文件标签
    tag_list = Tag.objects.all()
    return locals()


def register(request):
    try:
        if request.method == 'GET':
            userinfo = UserInfoModelForm()
            return render(request, 'register.html', locals())
        elif request.method == 'POST':
            userinfo = UserInfoModelForm(request.POST)
            if userinfo.is_valid():
                userinfo.save()
        return redirect('/')
    except Exception as e:
        print(e)


class BaseResponse:     # 用于生成返回给ajax回调函数的字典，obj = BaseResponse() obj.__dict__
    def __init__(self):
        self.status = True
        self.summery = None
        self.error = None
        self.data = None


def send_msg(request):
    obj = BaseResponse()
    dic = obj.__dict__
    return HttpResponse(json.dumps(dic))


def usercenter(request, name):
    try:
        if request.method == 'GET':
            u = User.objects.filter(username=name).first()
            user = UserInfoModelForm(instance=u)
            print(request.path)
            return render(request, 'usercenter.html', locals())
    except Exception as e:
        print(e)
    return render(request, 'login.html')


def useredit(request, name):
    if request.method == 'GET':
        u = User.objects.filter(username=name).first()
        user = UserInfoModelForm(instance=u)
        return render(request, 'useredit.html', locals())
    if request.method == 'POST':
        u = User.objects.filter(username=name).first()
        user = UserInfoModelForm(request.POST, instance=u)
        print(user)
        if user.is_valid():
            user.save()
        return HttpResponse('修改成功！<script language=\"javascript\">window.opener=null;window.close();</script>')


def islogin(request):
    v = request.session.get('username', None)
    if not v:
        login_status = "<a href='/'>登录</a>|<a href='/register'>注册</a>"
    else:
        login_status = "当前用户：<a href='/user/%s'>%s</a> | <a href='/logout/'>注销</a>" % (v, v)
    return v,login_status


def logout(request):
    request.session.clear()
    return redirect('/index')


def index(request, *args):

    v, login_status = islogin(request)
    try:
        article_list = Article.objects.all()
        article_list = get_page(request,article_list)
    except Exception as e:
        print(e)
    return render(request, 'index.html', locals())


def tar(request, *args):
    v, login_status = islogin(request)
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)
        article_list = get_page(request,article_list)
    except Exception as e:
        print(e)
    return render(request, 'tar.html', locals())


def tag(request):
    v, login_status = islogin(request)
    try:
        tagname = request.GET.get('tagname', None)
        if tagname == 'all':
            article_list = Article.objects.all()
        else:
            article_list = Article.objects.filter(tag__name=tagname)
        article_list = get_page(request,article_list)
    except Exception as e:
        print(e)
    return render(request, 'tag.html', locals())


def get_page(request,article_list):
    if request.COOKIES.get('per_page_count'):
        cookie_num = int(request.COOKIES.get('per_page_count'))
    else:
        cookie_num = 2
    page_count = cookie_num
    paginator = Paginator(article_list, page_count)
    try:
        page = int(request.GET.get('page', 1))  # 这两句不太懂
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


def article_desc(request, *args):
    v, login_status = islogin(request)
    try:
        article_id = int(request.GET.get('article_id', None))
        article_desc_list = Article.objects.get(id=article_id)
        print(article_desc_list)
        comment_list = Comment.objects.filter(article_id=article_id)
        # 处理评论
        if request.method == 'POST':
            # user = request.POST.get('user_name')
            # current_user = User(username=user)
            # current_user.save()
            comment = request.POST.get('user_comment')
            print(article_id)
            print(comment)
            # id = request.GET.get('article_id')

            user1 = User.objects.get(username=v)
            print(user1)
            comments = Comment(content=comment, article_id=article_id, user=user1)
            comments.save()
            # return HttpResponseRedirect('/article/')
            # print('11111')
    except Exception as e:
        print(e)
    return render(request, 'article.html', locals())


def uploadfile(request):
    # todo 未解决上传一次图片后再点击上传按钮时无法弹出上传框的问题
    filename = str(request.FILES.get('imgFile'))
    filepath = os.path.join(settings.BASE_DIR, 'uploads', str(datetime.datetime.today().year), str(datetime.datetime.today().month))
    if os.path.isdir(filepath):
        pass
    else:
        os.makedirs(filepath)
    with open(os.path.join(filepath, filename), 'wb') as f:
        img = request.FILES.get('imgFile')
        for i in img.chunks():
            f.write(i)
    dic = {
        'error': 0,
        'url': os.path.join('/', 'uploads', str(datetime.datetime.today().year), str(datetime.datetime.today().month), filename),
        'message': 'no problem'
    }
    return HttpResponse(json.dumps(dic))


def article_tc(request, **kwargs):
    tag_id = int(kwargs['tag'])
    category_id = int(kwargs['category_id'])
    tags = Tag.objects.all()
    category = Category.objects.all()
    if tag_id == 0 and category_id == 0:
        articles = Article.objects.all()
    elif tag_id == 0:
        articles = Article.objects.filter(category_id=category_id)
    elif category_id == 0:
        t = Tag.objects.get(id=tag_id)
        articles = t.article_set.all()
    else:
        t = Tag.objects.get(id=tag_id)
        articles = t.article_set.all().filter(category_id=category_id)
    print(articles)
    return render(request, 'article_select.html', locals())




