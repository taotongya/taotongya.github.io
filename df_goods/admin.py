from django.contrib import admin
from .models import *
# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
	list_display = ['id','ttitle']
	
class GoodsInfoAdmin(admin.ModelAdmin):
	list_display = ['id','gtitle','gprice','gkucun','gcontent','gtype']
	list_per_page = 15    #一列最多15个数据
	
admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)