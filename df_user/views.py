from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from hashlib import sha1
from df_user.models import *
from .islogin import *
from df_goods.models import *

# Create your views here.
def register(request):
    context = {'title':'注册'}
    return render(request, 'df_user/register.html', context)
	
def register_handle(request):
    # 接收用户输入信息
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    #print(uname, upwd, ucpwd, uemail)
    
    # 判断两次输入的密码是否一致
    if upwd != ucpwd:
        return HttpResponseRedirect('/df_user/register')
    
    # 对密码原文进行sha1的加密
    # 创建sha1的对象
    s1 = sha1()
    # 对passswd进行sha1的加密
    #s1.update(passwd) # python2的写法
    s1.update(upwd.encode()) # python3的写法
    upwd2 = s1.hexdigest()
    
    # 创建对象 填入数据 然后插入数据库中
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = uemail
    user.save()
    
    return HttpResponseRedirect('/df_user/login')
	
	
def register_exist(request):
    # 接收用户传入的uname参数
    get = request.GET
    uname = get.get('uname')
    
    # 在数据库中查找是否有该用户名
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})
	
def login(request):
	context = {'title':'登入'}
	return render(request, 'df_user/login.html', context)
	
def login_handle(request):
    # 接收用户输入信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu')
    
    # 根据用户名和密码查询数据库
    users = UserInfo.objects.filter(uname = uname)
    if len(users) >= 1:
        #print(users[0].upwd)
    
        # 对密码原文进行sha1的加密
        # 创建sha1的对象
        s1 = sha1()
        #s1.update(passwd) # python2的写法
        s1.update(upwd.encode()) # python3的写法
        upwd2 = s1.hexdigest()
    
        # 和数据库中的密文进行比较
        if upwd2 == users[0].upwd:
            url = request.COOKIES.get('url', '/df_user/info')
            red = HttpResponseRedirect(url) 
        
            if jizhu:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '')

            # 登录成功
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
                    
            return red
        else:
            # 登录失败，密码错误
            context = {'title':'登录','error_pwd':1,'error_name':0}
            return render(request, 'df_user/login.html', context)

    else:
        # 用户名找不到
        context = {'title':'登录','error_name':1,'error_name':0}
        return render(request, 'df_user/login.html', context)
		
@islogin		
def info(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id = request.session['user_id']).uaddress
    user_phone = UserInfo.objects.get(id = request.session['user_id']).uphone
	
	 # 从cookies中读取最近浏览的信息
    goods_ids = request.COOKIES.get('goods_ids')
    if goods_ids and goods_ids != '':
        goods_ids = goods_ids.split(',')
    else:
        goods_ids = []
    # 遍历goods_ids列表 根据id搜索出每个产品 并添加到产品列表中
    goods_list = []
    for id in goods_ids:
        if id != '':
            goods = GoodsInfo.objects.get(id=id)
            goods_list.append(goods)
	
	
	
	
	
    context = {'title': '用户中心', 
               'user_name' : request.session['user_name'],
               'user_email' : user_email,
               'user_address': user_address,
               'user_phone': user_phone,
			   'page_name': 1,
			   'info':1,
			   'goods_list':goods_list}
    return render(request, 'df_user/user_center_info.html',context)
	
@islogin
def order(request):
	context = {'title':'全部订单',
				'page_name': 1,
				'order':1}
	return render(request,'df_user/user_center_order.html', context)

	
@islogin
def site(request):
    user = UserInfo.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        # 当用户通过表单提交信息的时候 request.method="POST" 此时获取提交过来的参数 并保存到数据库中
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    else:
        # 当用户通过url直接访问df_user/site 的时候 request.method="GET" 此时无需进行任何操作 直接通过模型类获取属性即可
        pass
    
    context = {'title': '用户中心',
               'ushou' : user.ushou,
               'uaddress': user.uaddress,
               'uphone': user.uphone,
			   'page_name': 1,
               'site': 1}
    return render(request, 'df_user/user_center_site.html', context)
	
def logout(request):
    request.session.flush() # 清理session缓存
    return HttpResponseRedirect('/df_user/login')

		
	
	
	
	
	
	
	
	
	
	
	
	
	

	