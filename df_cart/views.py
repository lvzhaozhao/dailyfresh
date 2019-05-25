from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse

from df_user.utils import login_required
from df_cart.models import CartModel
from common.common import cart_count_goods
# Create your views here.


@login_required
def cart(request):
    """购物车"""
    user_id = request.session["user_id"]
    carts = CartModel.objects.filter(user_id=user_id)

    return render(request, "df_cart/cart.html", {"carts": carts, "cart_count": len(carts), "title": "购物车"})


@login_required
def add(request, goods_id, count):
    user_id = request.session.get("user_id")

    # 查询购物车中是否已经有这个商品在这个人的名下，如果有，那么增加商品的数量，如果没有，新建一个
    carts = CartModel.objects.filter(user_id=user_id, goods_id=goods_id)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count +count
    else:
        cart = CartModel()
        cart.user_id = user_id
        cart.count = count
        cart.goods_id = goods_id
    cart.save()

    # 如果是ajax请求则返回一个json，否则跳转到购物车
    if request.is_ajax():
        cart_count = cart_count_goods(request, CartModel)
        return JsonResponse({"cart_count": cart_count})
    return redirect(reverse("cart:cart"))


@login_required
def delete(request, cart_id):
    """从购物车中删除某个商品"""
    try:
        cart = CartModel.objects.get(id=cart_id)
    except:
        # 前后端尽量不要以bool类型来传递数据
        return JsonResponse({"success": 0})
    cart.delete()
    return JsonResponse({"success": 1})


@login_required
def update(request, cart_id, count):
    """更新购物车内的购买商品数量"""
    cart = CartModel.objects.get(id=cart_id)
    cart.count = count
    cart.save()
    return JsonResponse({"success": 1})
