from django.http.response import HttpResponse, HttpResponseRedirect



def islogin(func):
    def login_fun(request, *args, **kwargs):
        # 判断是否登录
        if request.session.get('user_id'):
            # 如果已经登录 正常访问页面
            return func(request, *args, **kwargs)
        else:
            # 如果未登录 则跳转到登录页面
            red = HttpResponseRedirect('/df_user/login')
            # 缓存路径 登录后自动调回原先要访问的页面
            red.set_cookie('url', request.get_full_path()) 
            return red
    return login_fun
	
if __name__ == '__main__':
    @islogin
    def order(request, typeid):
        print('order')
        return 'haha'

    ret = order('request', 3)
    print(ret)