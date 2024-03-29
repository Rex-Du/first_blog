# coding:utf-8
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# 自定义文章的管理器
class ArticeManage(models.Manager):
    def date_format(self):
        date_list = Article.objects.values('date_publish')
        date_format_list = []
        for date in date_list:
            date_format = date['date_publish'].strftime('%Y-%m')
            if date_format not in date_format_list:
                date_format_list.append(date_format)
        return date_format_list


# 用户模型.
# 第一种：采用的继承方式扩展用户信息（本系统采用）
# 扩展：关联的方式去扩展用户信息
# class UserGroup(models.Model):
#     # user = models.ForeignKey(User, verbose_name='用户')
#     groupname = models.CharField('用户组名',max_length=20,null=False)
#
#     class Meta:
#         verbose_name = '用户组'
#
#     def __str__(self):
#         return self.groupname

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True, null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username



# tag(标签)
class Tag(models.Model):
    name = models.CharField('标签名称',max_length=30)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类
class Category(models.Model):
    name = models.CharField('分类名称',max_length=30)
    index = models.IntegerField('分类的排序',default=999)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=False, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类', on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    objects = ArticeManage()
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章', on_delete=models.DO_NOTHING)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return str(self.id)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200,  verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title