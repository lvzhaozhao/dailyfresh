import string, random, time, re, datetime
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from df_user.forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from df_user.models import UserModel, Address
from df_user.utils import login_required
from df_goods.models import GoodsModel
from df_order.models import OrderGoodsModel, OrderModel


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            username_or_email = login_form.cleaned_data['username_or_email']
            auth.login(request, user)
            request.session["user_id"] = user.id
            request.session["username_or_email"] = username_or_email
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()
    return render(request, 'df_user/login.html', {'login_form': login_form})


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = UserModel.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['register_code']
            # # 登录用户
            # user = auth.authenticate(username=username, password=password)
            # auth.login(request, user)
            return redirect(request.GET.get('from', reverse('user:login')))
    else:
        reg_form = RegForm()
    return render(request, 'df_user/register.html', {'reg_form': reg_form})


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('user:login')))


def change_nickname(request):
    redirect_to = request.GET.get('form', reverse('index'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            username_new = form.cleaned_data['username_new']
            profile = UserModel.objects.get(email=request.user.email)
            print(profile)
            profile.username = username_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改用户名'
    context['form_title'] = '修改用户名'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'df_user/form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('user:info'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'df_user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bing_email_code'] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now

        # 发送邮件
        send_mail(
            '绑定邮箱',
            '验证码: %s' % code,
            '296689155@qq.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    redirect_to = reverse('index')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'df_user/form.html', context)


def forgot_password(request):
    redirect_to = reverse('user:login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = UserModel.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'df_user/forgot_password.html', context)


@login_required
def user_center_info(request):
    """用户中心"""
    user_id = request.session["user_id"]
    user = UserModel.objects.get(id=user_id)
    add = Address.objects.filter(user_id=user.id).last()
    # 从session中拿到商品id的列表（商品详情里写入session的）
    goods_id_list = request.session.get(str(user_id), [])
    # 用户最近浏览的商品记录
    goods_list = []
    # 通过遍历商品id列表，拿到商品对象组成一个有序的商品对象列表
    for goods_id in goods_id_list:
        goods_list.append(GoodsModel.objects.get(id=goods_id))
    if add == None:
        phone = '无'
    else:
        phone = add.phone
    if add == None:
        address = '无'
    else:
        address = add.addr
    # goods_list = GoodsModel.objects.filter(id__in=goods_id_list)
    return render(request, "df_user/user_center_info.html", {"user": user, "goods_list": goods_list, 'phone': phone, 'address': address})


@login_required
def user_center_order(request, page_num):
    """用户订单中心"""
    user_id = request.session["user_id"]
    user = UserModel.objects.get(id=user_id)
    orders = OrderModel.objects.filter(user=user).order_by('-create_time')
    # print(orders)
    ord_status = OrderModel.ORDER_status_dic
    for order in orders:
        ps = OrderGoodsModel.objects.filter(order=order)
        for amount in ps:
            # 动态为每个订单提供小计
            total = amount.goods.price * amount.number
            amount.total = total
        # 动态为每个订单提供订单下所有商品信息
        order.ps = ps
        # 获取订单的状态
        order.status = ord_status[str(order.order_status)]
        # 获取订单编号
        order_time = order.create_time
        time_stamp = int(time.mktime(order_time.timetuple()))
        order.time_stamp = time_stamp
    # 使用Django内置分页，每页显示1个订单
    page_manage = Paginator(orders, 3)
    try:
        # 创建Page对象，如果页面取不到，得到第一个页面page对象
        page = page_manage.page(page_num)
    except EmptyPage:
        page = page_manage.page(1)
    # 控制页码显示5页
    total_page_num = page_manage.num_pages
    if total_page_num < 5:
        show_nums = range(1, total_page_num + 1)
    elif page_num <= 3:
        show_nums = range(1, 6)
    elif total_page_num - page_num <= 2:
        show_nums = range(page_num - 4, total_page_num + 1)
    else:
        show_nums = range(page_num - 2, page_num + 3)

    context = {
        'orders': orders,
        'page': page,
        'show_nums': show_nums,
    }
    return render(request, 'df_user/user_center_order.html', context)


@login_required
def user_center_site(request):
    """收货地址"""
    # 地址的添加
    if request.method == 'POST':
        # 接受数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'df_user/user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'df_user/user_center_site.html', {'errmsg': '手机号格式不正确'})

        # 业务处理：地址添加
        # 如果用户已经存在默认收货地址，添加的地址不作为默认地址
        # 获取登录用户对应的User对象
        user = request.user

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答，刷新地址页面
        return redirect(reverse('user:site'))  # get请求方式

    # 获取用户的地址信息
    # 获取登录用户对应的User对象
    user = request.user
    # address = Address.objects.get_default_address(user)
    address = Address.objects.filter(user_id=user.id).last()
    if address == None:
        address = '无'
    else:
        address.phone = address.phone[:3] + '****' + address.phone[7:]
        address = address

    # 使用模板
    return render(request, 'df_user/user_center_site.html', {'page': 'address', 'address': address})

