"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blog.views import views, account
urlpatterns = [
    # url(r'^login$', views.login, name='login'),
    url(r'^check_code.html$', account.check_code),
    url(r'^check_text', account.check_code),
    url(r'^register/', views.register, name='register'),
    url(r'^send_msg/', views.send_msg, name='send_msg'),
    url(r'^user/(?P<name>\S+)', views.usercenter, name='usercenter'),
    url(r'^edit-(?P<name>\S+)', views.useredit, name='useredit'),
    url(r'^index/', views.index, name='index'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^tar/', views.tar, name='tar'),
    url(r'^tag/', views.tag, name='tag'),
    url(r'^article/', views.article_desc, name='article_desc'),
    url(r'^uploadfile/', views.uploadfile, name='uploadfile'),
    # url(r'^article_select/', views.article_select, name='article_select'),
    url(r'^(?P<tag>\d+)-(?P<category_id>\d+)$', views.article_tc, name='article_tc'),
    # url(r'^comments/', submit_comments, name='submit_comments'),
]
