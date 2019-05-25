from django.http import HttpResponseRedirect
from django.shortcuts import reverse


# 判断是否登录，如果没有登录就跳转到登录页面
def login_required(func):
    def login_func(request, *args, **kwargs):
        # 判断session中是否有user_id，如果没有则认为该用户没有登陆
        if request.session.has_key("user_id"):
            return func(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect(reverse("user:login"))
            # 把访问的路径存入到cookie中 key：next_url
            response.set_cookie("next_url", request.get_full_path())
            return response
    return login_func
