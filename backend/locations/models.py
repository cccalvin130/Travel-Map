from django.db import models


class Location(models.Model):
    """
    地点模型 - 存储用户访问过的所有地点信息

    这个模型对应需求中的：
    - 2. Add Visited Places (添加访问地点)
    - 5. Location Information (地点信息)
    - 8. Data Storage (数据存储)

    数据库中会生成一张名为 locations_location 的表，
    每个地点就是表中的一行记录。
    """

    # 地点名称 - 用户给这个地点起的名字，比如 "巴黎铁塔"
    # max_length=200 表示最多200个字符，足够存任何地点名称
    name = models.CharField(max_length=200, verbose_name="地点名称")

    # 国家 - 比如 "法国"
    country = models.CharField(max_length=100, verbose_name="国家")

    # 城市 - 比如 "巴黎"
    city = models.CharField(max_length=100, verbose_name="城市")

    # 纬度 - 地理坐标，用于在地图上标记位置
    # DecimalField 可以精确存储小数，max_digits=9 总位数，decimal_places=6 小数位
    # 纬度范围是 -90 到 90，这样的精度足够定位到几米之内
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="纬度"
    )

    # 经度 - 地理坐标
    # 经度范围是 -180 到 180
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="经度"
    )

    # 访问日期 - 用户什么时候去的这个地方
    # DateField 只存日期（年-月-日），不存具体时间
    # null=True, blank=True 表示这个字段可以为空（用户可能不记得具体日期）
    visit_date = models.DateField(
        null=True, blank=True, verbose_name="访问日期"
    )

    # 个人笔记 - 用户对这个地点的描述或回忆
    # TextField 可以存很长的文本，没有长度限制
    # blank=True 表示可以不填
    notes = models.TextField(blank=True, verbose_name="个人笔记")

    # 创建时间 - 这条记录什么时候被创建的
    # auto_now_add=True 表示创建时自动填入当前时间，之后不会改变
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 更新时间 - 这条记录最后一次被修改的时间
    # auto_now=True 表示每次保存时自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # Meta 类是 Django 模型的配置选项
        # verbose_name 是在后台管理界面显示的单数名称
        verbose_name = "访问地点"
        # verbose_name_plural 是复数名称
        verbose_name_plural = "访问地点"
        # 默认按访问日期倒序排列（最新的在前面），如果日期为空则按创建时间倒序
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        # __str__ 方法定义这个对象被打印时显示什么
        # 比如在后台管理列表里，每个地点会显示 "巴黎铁塔 (法国, 巴黎)"
        return f"{self.name} ({self.country}, {self.city})"


class Photo(models.Model):
    """
    照片模型 - 存储每个地点的照片

    这个模型对应需求中的：
    - 4. Photo Management (照片管理)
    - 8. Data Storage (数据存储)

    设计思路：一个地点可以有多张照片，所以用外键(ForeignKey)关联到 Location。
    这是数据库中典型的"一对多"关系：一个地点 → 多张照片。
    """

    # 外键 - 这张照片属于哪个地点
    # ForeignKey 建立"多对一"关系：多张照片对应一个地点
    # on_delete=models.CASCADE 表示：如果地点被删除了，这个地点的所有照片也一起删除
    # related_name='photos' 让我们可以通过 location.photos 来获取这个地点的所有照片
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="所属地点"
    )

    # 图片文件 - 用户上传的照片
    # ImageField 专门用来存图片，会自动验证上传的是不是图片
    # upload_to='location_photos/' 表示图片会存在 media/location_photos/ 文件夹下
    image = models.ImageField(
        upload_to='location_photos/',
        verbose_name="图片"
    )

    # 图片描述 - 给这张照片加个说明，比如 "夕阳下的铁塔"
    # blank=True 表示可以不填
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="图片描述"
    )

    # 上传时间 - 这张照片什么时候上传的
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    class Meta:
        verbose_name = "照片"
        verbose_name_plural = "照片"
        # 默认按上传时间倒序排列（最新上传的在前面）
        ordering = ['-uploaded_at']

    def __str__(self):
        # 显示为 "巴黎铁塔 - 照片1" 这样的格式
        return f"{self.location.name} - {self.description or '照片'}"
