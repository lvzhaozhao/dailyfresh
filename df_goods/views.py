from django.shortcuts import render
from django.core.paginator import Paginator

from df_goods.models import GoodsModel, CategoryModel
from df_cart.models import CartModel
from common.common import cart_count_goods
# Create your views here.


def index(request):
    """首页"""
    # 拿出所有的分类
    category_list = CategoryModel.objects.all()
    # 分别取出分类下的最新商品
    new_goods_dict = {}  # 用来存储每个分类下的最新商品
    for category in category_list:
        goods_info_list = GoodsModel.objects.filter(category_id=category.id).order_by("-id")[:4]
        # apple_list = GoodsModel.objects.filter(category_id=category.id, )
        new_goods_dict[category] = goods_info_list
    cart_count = cart_count_goods(request, CartModel)
    if not cart_count:
        cart_count = 0
    return render(request, "index.html", {"new_goods_dict": new_goods_dict, "category_list": category_list, "cart_count": cart_count})


def search_detail(request):
    search = request.GET.get("search")
    categorys = CategoryModel.objects.all()
    goods_lists = GoodsModel.objects.filter(goods_name__icontains=search)
    data = {
        "goods_lists": goods_lists,
        "search": search,
        "categorys": categorys,
    }
    return render(request, 'search.html', data)


def goods_list(request, category_id, sort, page_num):
    """商品列表视图"""
    """
    category_id 分类的id
    page_num 获取当前页的页码
    sort 排序的字段 默认：default 价格：price 人气：popular
    """
    category = CategoryModel.objects.get(id=category_id)
    categorys = CategoryModel.objects.all()
    # 取该类型的最新的两个商品
    news = GoodsModel.objects.filter(category_id=category_id).order_by("-id")[:2]

    goods_list = []
    goods_query_set = GoodsModel.objects.filter(category_id=category_id)
    if sort == "default":  # 默认排序 最新的在上面
        goods_list = goods_query_set.order_by("-id")
    elif sort == "price":
        goods_list = goods_query_set.order_by("-price")
    elif sort == "popular":
        goods_list = goods_query_set.order_by("-popular")

    # 根据商品的列表goods_list，进行分页
    paginator = Paginator(goods_list, 3)
    page = paginator.page(page_num)

    cart_count = cart_count_goods(request, CartModel)
    context = {
        "category": category,
        "categorys": categorys,
        "news": news,
        "sort": sort,
        "goods_list": goods_list,
        "page": page,
        "page_num": int(page_num),
        "cart_count": cart_count,
    }
    return render(request, "df_goods/list.html", context)


def detail(request, goods_id):
    """某个商品的详细信息，goods id是具体的某个商品"""
    goods = GoodsModel.objects.get(id=goods_id)
    goods.popular = goods.popular + 1
    goods.save()
    news = goods.category.goodsmodel_set.order_by("-id")[:2]
    # 记录最近的浏览记录，在用户中心使用
    # 判断是否已经登录
    if request.session.has_key("user_id"):
        user_id = request.session.get("user_id")
        goods_id_list = request.session.get(str(user_id), [])
        if not goods_id_list:  # 判断是否有浏览记录
            goods_id_list.append(goods.id)
        else:
            # 如果已经存在过浏览的商品大于5个时 删除一个
            if goods_id in goods_id_list:
                goods_id_list.remove(goods_id)
            # 添加元素到列表的第一个
            goods_id_list.insert(0, goods_id)
            # 判断是否超过五个记录，超过删除最后一个
            if len(goods_id_list) > 5:
                del goods_id_list[-1]
        request.session[user_id] = goods_id_list
    cart_count = cart_count_goods(request, CartModel)
    categorys = CategoryModel.objects.all()
    return render(request, "df_goods/detail.html", {"goods": goods, "news": news, "cart_count": cart_count, 'categorys': categorys})
