from django.shortcuts import render
from django.http import JsonResponse
from df_user.utils import login_required
from df_goods.models import GoodsModel
from df_user.models import UserModel, Address
from df_cart.models import CartModel
from df_order.models import OrderModel, OrderGoodsModel
# Create your views here.


@login_required
def order(request, good_id):
    """订单页面"""
    user_id = request.session.get("user_id")
    user = UserModel.objects.get(id=user_id)
    goods = GoodsModel.objects.get(id=good_id)
    print(goods)
    add = Address.objects.filter(user_id=user.id).last()
    if add == None:
        add = '无'
    else:
        add.phone = add.phone[:3] + '****' + add.phone[7:]
        add = add
    context = {
        # "good_id": good_id,
        "title": "订单页面",
        "user": user,
        "goods": goods,
        'add': add,
        'count': 1,
    }
    return render(request, "df_order/order.html", context)


@login_required
def order_main(request):
    """订单页面"""
    user_id = request.session.get("user_id")
    user = UserModel.objects.get(id=user_id)
    cart_id_list = request.GET.getlist("cart_id_list")
    add = Address.objects.filter(user_id=user.id).last()
    # 根据购物车的id，查询出对应的商品
    cart_info_list = []
    for cart_id in cart_id_list:
        cart = CartModel.objects.get(id=cart_id)
        cart_info_list.append(cart)
    if add == None:
        add = '无'
    else:
        add.phone = add.phone[:3] + '****' + add.phone[7:]
        add = add
    context = {
        "title": "订单页面",
        "user": user,
        "cart_info_list": cart_info_list,
        'add': add
    }
    return render(request, "df_order/order_main.html", context)


@login_required
def add_order(request):
    """添加订单到数据库"""
    cart_list = request.POST.getlist("cart_list", [])
    total_price = request.POST.get("total_price", 0)
    user_id = request.session.get("user_id")

    order = OrderModel()
    order.user_id = user_id
    order.total_price = total_price
    order.is_pay = 0
    order.save()

    for cart_id in cart_list:
        cart = CartModel.objects.get(id=cart_id)

        order_goods = OrderGoodsModel()
        order_goods.goods_id = cart.goods_id
        order_goods.order_id = order.id
        order_goods.number = cart.count
        order_goods.save()

        # 订单信息和订单对应的商品信息保存完毕，删除购物车中的商品
        cart.delete()
    return JsonResponse({"result": "success"})

