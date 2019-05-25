# 统计购物车内商品的数量
def cart_count_goods(request, CartModel):
    # 从session中拿到user的id
    cart_count = 0
    user_id = request.session.get("user_id", -1)
    carts = CartModel.objects.filter(user_id=user_id)
    for cart in carts:
        cart_count += cart.count
    return cart_count

