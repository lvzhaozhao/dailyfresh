from haystack import indexes
from df_goods.models import GoodsModel


# 这个文件的作用是设置haystack在生成索引的时候，根据哪些字段来生成索引
# 名字是需要检索的model的名字+Index
class GoodsModelIndex(indexes.SearchIndex, indexes.Indexable):
    # 创建一个字段
    # 每一个索引里必须要有而且只能有一个字段document=True
    text = indexes.CharField(document=True, use_template=True)

    # 必须重载
    def get_model(self):
        return GoodsModel

    # 重载index_queryset函数
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
