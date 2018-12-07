from django.shortcuts import render
from .models import *
# Create your views here.
def cart(request):
	# 从session中获取当前用户的id
	uid = request.session.get('user_id')
	# 根据id搜索当前用户放入购物车的品种和数量
	carts = CartInfo.objects.filter(user_id = 1)
	context = {'title':'购物车',
			   'page_name':1,
			   'carts':carts}
	return render(request, 'df_cart/cart.html', context)