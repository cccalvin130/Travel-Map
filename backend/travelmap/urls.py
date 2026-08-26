"""
URL configuration for travelmap project.

主路由配置文件 - 所有网址都从这里开始分配
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django 后台管理界面
    path('admin/', admin.site.urls),

    # 我们的 API 接口
    # 所有以 api/ 开头的网址，都交给 locations 应用的 urls.py 处理
    # 比如 /api/locations/ 会匹配到 locations/urls.py 里的 'locations/'
    path('api/', include('locations.urls')),
]

# 配置媒体文件（用户上传的图片）的访问路径
# 这只在开发环境(DEBUG=True)下生效，生产环境需要用 Nginx 等服务器来处理静态文件
# 意思是：当访问 /media/xxx.jpg 时，Django 会去 MEDIA_ROOT 目录下找这个文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
