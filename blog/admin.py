from django.contrib import admin
from blog.models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc','desc','content', 'click_count','date_publish')

    class Media:
        js = ( '/static/js/kindeditor-4.1.10/kindeditor-min.js',
               '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
               '/static/js/kindeditor-4.1.10/config.js',
            )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Links)
admin.site.register(Ad)
admin.site.register(Comment)
