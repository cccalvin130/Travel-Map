from django.contrib import admin
from .models import Location, Photo


class PhotoInline(admin.TabularInline):
    """
    照片内联编辑 - 在地点编辑页面里直接管理该地点的照片

    为什么用 TabularInline？
    因为一个地点有多张照片，我们希望在编辑地点时，
    能在同一个页面里直接添加、编辑、删除照片，
    而不用跳转到另一个页面去管理照片。
    TabularInline 会以表格形式显示照片，比较紧凑。
    """
    model = Photo
    # 额外显示几个空行，方便直接添加新照片
    extra = 1
    # 显示的字段
    fields = ['image', 'description', 'uploaded_at']
    # 只读字段（上传时间自动生成，不能手动改）
    readonly_fields = ['uploaded_at']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    地点后台管理配置

    这个类定义了在 Django Admin 后台里，地点模型如何显示和管理。
    """

    # 列表页显示的字段（每一列是什么）
    list_display = [
        'name',           # 地点名称
        'country',        # 国家
        'city',           # 城市
        'visit_date',     # 访问日期
        'photo_count',    # 照片数量（自定义方法）
        'created_at',     # 创建时间
    ]

    # 可以搜索的字段（顶部搜索框会搜这些字段）
    search_fields = ['name', 'country', 'city', 'notes']

    # 右侧筛选器（可以按这些字段过滤）
    list_filter = ['country', 'city', 'visit_date']

    # 编辑页的字段分组（把相关字段放在一起）
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'country', 'city']
        }),
        ('地图坐标', {
            'fields': ['latitude', 'longitude']
        }),
        ('访问信息', {
            'fields': ['visit_date', 'notes']
        }),
        ('系统信息', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']  # 默认折叠起来
        }),
    ]

    # 只读字段（创建和更新时间自动生成，不能手动改）
    readonly_fields = ['created_at', 'updated_at']

    # 内联编辑：在地点编辑页里直接管理照片
    inlines = [PhotoInline]

    def photo_count(self, obj):
        """
        自定义方法：计算这个地点有多少张照片
        在列表页显示照片数量
        """
        return obj.photos.count()
    # 给这个方法设置一个显示名称
    photo_count.short_description = '照片数量'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    照片后台管理配置

    虽然照片可以在地点编辑页里内联管理，
    但我们也单独注册一下，这样可以在照片列表页统一管理所有照片。
    """

    # 列表页显示的字段
    list_display = [
        'location',       # 所属地点
        'description',    # 图片描述
        'uploaded_at',    # 上传时间
    ]

    # 可以搜索的字段
    search_fields = ['location__name', 'description']

    # 右侧筛选器
    list_filter = ['uploaded_at', 'location__country']

    # 只读字段
    readonly_fields = ['uploaded_at']
