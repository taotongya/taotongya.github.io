from django.shortcuts import render
from django.core.paginator import Paginator
from df_goods.models import *
# Create your views here.
def index(request):
    
    fruit = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[:4] # 最新产品
    fruit2 = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[:3] # 热销产品
    fish = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[:4] # 最新产品
    fish2 = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[:3] # 热销产品
    meat = GoodsInfo.objects.filter(gtype_id=3).order_by('-id')[:4] # 最新产品
    meat2 = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[:3] # 热销产品
    egg = GoodsInfo.objects.filter(gtype_id=4).order_by('-id')[:4] # 最新产品
    egg2 = GoodsInfo.objects.filter(gtype_id=4).order_by('-gclick')[:3] # 热销产品
    vegetable = GoodsInfo.objects.filter(gtype_id=5).order_by('-id')[:4] # 最新产品
    vegetable2 = GoodsInfo.objects.filter(gtype_id=5).order_by('-gclick')[:3] # 热销产品
    frozen = GoodsInfo.objects.filter(gtype_id=6).order_by('-id')[:4] # 最新产品
    frozen2 = GoodsInfo.objects.filter(gtype_id=6).order_by('-gclick')[:3] # 热销产品
    
    context = {'title': '首页',
               'fruit':fruit, 'fruit2':fruit2,
               'fish':fish, 'fish2':fish2,
               'meat':meat, 'meat2':meat2,
               'egg':egg, 'egg2':egg2,
               'vegetable':vegetable, 'vegetable2':vegetable2,
               'frozen':frozen, 'frozen2':frozen2,
               'guest_cart':1}
    return render(request, 'df_goods/index.html', context)
	
def goodlist(request, typeid, pageid, sort):
#获取产品的类型
	goodtype = TypeInfo.objects.get(id = typeid)
    #获取最新产品
	newgood = GoodsInfo.objects.all().order_by('-id')[:2]
	#根据sort的值决定排序方式
	if sort == '1':  #所以产品按最新排序
		sumGoodList = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')
	elif sort == '2': # 按价格排序
		sumGoodList = GoodsInfo.objects.filter(gtype_id=typeid).order_by('gprice')
	elif sort == '3': # 按人气排序
		sumGoodList = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-gclick')
	
	
    # 分页
	paginator = Paginator(sumGoodList, 15)
	goodList = paginator.page(int(pageid))
	pindexlist = paginator.page_range # 所有页的id（搜索）
	
    
	context = {'title': '商品列表',
               'guest_cart': 1,
               'newgood': newgood,
			   'goodList': goodList,
			   'typeid':typeid,
			   'sort':sort,
			   'pindexlist':pindexlist,
			   'pageid':int(pageid),
			   'goodtype':goodtype}
	return render(request, 'df_goods/list.html', context)
	
	
def detail(request, id):
	#获取商品的对象
	goods = GoodsInfo.objects.get(id=id)
    # 获取最新发布的商品
	newgood = GoodsInfo.objects.all().order_by('-id')[:2]
	#点击量
	goods.gclick = goods.gclick + 1
	goods.save()
    # 获取类型的id
	typeid = goods.gtype_id
    # 获取产品类型
	goodtype = goods.gtype
    
	
	context = {'title': '商品详情',
               'guest_cart': 1,
			   'g':goods,
               'newgood': newgood,
               'typeid':typeid,
               'goodtype': goodtype,
			   'isDewtail':1}
	response = render(request, 'df_goods/detail.html', context)
	
	#读取请求的cookies
	goods_ids = request.COOKIES.get('goods_ids')
	#判断cookies中的商品ID序列是否为空
	if goods_ids and goods_ids != '':
	#不为空以逗号进行分割，把字符串转换为列表
		goods_ids = goods_ids.split(',')
		#如果列表中已有当前ID，则需移除
		if id in goods_ids:
			goods_ids.remove(id)
		#把当前ID放在最前面
		goods_ids.insert(0,id)
		#如果超过5个，则保留前5个
		if len(goods_ids) > 5:
			goods_ids = goods_ids[0:5]
	else:
	   #为空
		goods_ids = id
		#把列表重新拼接成字符串
	goods_ids = ','.join(goods_ids)
	#把响应数据存储到COOKIES中
	response.set_cookie('goods_ids',goods_ids)
	return response	
	
		
		
		
		
		
		
		
		
	
	
	
	
	
	
	
	
	
	