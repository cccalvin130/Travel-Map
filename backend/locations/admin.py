from django.contrib import admin
from .models import Location, Photo

# 把 Location 模型注册到后台管理界面
# 注册之后，就能在 http://127.0.0.1:8000/admin/ 里看到并管理地点数据了
admin.site.register(Location)

# 把 Photo 模型注册到后台管理界面
# 注册之后，就能在后台里看到并管理照片数据了
admin.site.register(Photo)
