from django.urls import path
from . import views

"""
URL 路由配置 - 把网址和视图函数对应起来

命名规则：
- 列表页用复数名词，比如 /api/locations/
- 详情页用 /api/locations/<id>/
- 子资源用嵌套，比如 /api/locations/<id>/photos/
"""

urlpatterns = [
    # 地点列表：获取所有地点 / 创建新地点
    path('locations/', views.location_list, name='location-list'),

    # 地点详情：获取/更新/删除单个地点
    # <int:location_id> 表示从 URL 中提取一个整数，作为 location_id 参数传给视图
    path('locations/<int:location_id>/', views.location_detail, name='location-detail'),

    # 某个地点的照片列表：获取所有照片 / 上传新照片
    path('locations/<int:location_id>/photos/', views.photo_list, name='photo-list'),

    # 单张照片：删除照片
    path('locations/<int:location_id>/photos/<int:photo_id>/', views.photo_detail, name='photo-detail'),
]
