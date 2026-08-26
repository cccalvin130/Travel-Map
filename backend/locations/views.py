import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import Location, Photo


def location_to_dict(location):
    """
    工具函数：把 Location 对象转换成字典（方便转成 JSON 返回给前端）

    为什么需要这个函数？
    Django 的模型对象不能直接转成 JSON，需要手动把每个字段取出来，
    组装成 Python 字典，然后 JsonResponse 会自动把字典转成 JSON 字符串。

    返回的字典里还包含了这个地点的所有照片信息，这样前端一次请求就能拿到完整数据。
    """
    return {
        'id': location.id,
        'name': location.name,
        'country': location.country,
        'city': location.city,
        'latitude': float(location.latitude),   # Decimal 转 float，方便 JSON 序列化
        'longitude': float(location.longitude),
        # 用 str() 而不是 isoformat()，这样不管是 date 对象还是字符串都能正确处理
        'visit_date': str(location.visit_date) if location.visit_date else None,
        'notes': location.notes,
        'created_at': str(location.created_at),
        'updated_at': str(location.updated_at),
        # 把这个地点的所有照片也一起返回
        'photos': [
            {
                'id': photo.id,
                'image': photo.image.url,   # 图片的访问 URL
                'description': photo.description,
                'uploaded_at': str(photo.uploaded_at),
            }
            for photo in location.photos.all()
        ]
    }


@csrf_exempt
def location_list(request):
    """
    地点列表 API - 处理两个功能：
    - GET: 获取所有地点列表
    - POST: 创建一个新地点

    URL: /api/locations/
    """

    if request.method == 'GET':
        # ========== 获取所有地点 ==========
        # 从数据库查询所有地点，按模型里定义的 ordering 排序
        locations = Location.objects.all()
        # 把每个地点都转成字典，组成列表
        data = [location_to_dict(loc) for loc in locations]
        # 返回 JSON 格式的响应
        return JsonResponse({'locations': data, 'count': len(data)})

    elif request.method == 'POST':
        # ========== 创建新地点 ==========
        try:
            # 解析前端发来的 JSON 数据
            # request.body 是请求体的原始字节，用 json.loads 转成 Python 字典
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的 JSON 格式'}, status=400)

        # 从数据中提取各个字段
        # data.get('name', '') 表示：取 name 字段，如果不存在就用空字符串
        name = data.get('name', '').strip()
        country = data.get('country', '').strip()
        city = data.get('city', '').strip()

        # 验证必填字段
        # 地点名称、国家、城市是必填的，如果为空就返回错误
        if not name or not country or not city:
            return JsonResponse(
                {'error': '地点名称、国家、城市为必填项'},
                status=400
            )

        try:
            # 纬度和经度需要是数字，用 float() 转换
            # 如果转换失败（比如用户输入了文字），会抛出 ValueError，我们捕获并返回错误
            latitude = float(data.get('latitude', 0))
            longitude = float(data.get('longitude', 0))
        except (ValueError, TypeError):
            return JsonResponse({'error': '纬度和经度必须是数字'}, status=400)

        # 创建新的地点对象
        # Location.objects.create() 会创建对象并自动保存到数据库
        location = Location.objects.create(
            name=name,
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            visit_date=data.get('visit_date') or None,  # 如果是空字符串就存 None
            notes=data.get('notes', ''),
        )

        # 返回创建成功的响应，status=201 表示"已创建"
        return JsonResponse(
            {'message': '地点创建成功', 'location': location_to_dict(location)},
            status=201
        )

    else:
        # 如果是其他请求方法（比如 PUT、DELETE），返回 405 方法不允许
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def location_detail(request, location_id):
    """
    地点详情 API - 处理单个地点的查、改、删：
    - GET: 获取单个地点的详细信息
    - PUT: 更新地点信息
    - DELETE: 删除地点

    URL: /api/locations/<id>/
    location_id 参数是从 URL 里提取的地点 ID
    """

    # 先根据 ID 从数据库查找地点
    # Location.objects.filter(id=location_id).first() 会返回匹配的第一个对象，找不到就返回 None
    # 为什么不用 get()？因为 get() 找不到会抛异常，需要额外处理，用 filter().first() 更方便
    location = Location.objects.filter(id=location_id).first()

    # 如果找不到地点，返回 404 错误
    if not location:
        return JsonResponse({'error': '地点不存在'}, status=404)

    if request.method == 'GET':
        # ========== 获取单个地点 ==========
        return JsonResponse({'location': location_to_dict(location)})

    elif request.method == 'PUT':
        # ========== 更新地点 ==========
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的 JSON 格式'}, status=400)

        # 更新各个字段
        # 只有前端传了这个字段，我们才更新，否则保留原来的值
        if 'name' in data:
            location.name = data['name'].strip()
        if 'country' in data:
            location.country = data['country'].strip()
        if 'city' in data:
            location.city = data['city'].strip()
        if 'latitude' in data:
            try:
                location.latitude = float(data['latitude'])
            except (ValueError, TypeError):
                return JsonResponse({'error': '纬度必须是数字'}, status=400)
        if 'longitude' in data:
            try:
                location.longitude = float(data['longitude'])
            except (ValueError, TypeError):
                return JsonResponse({'error': '经度必须是数字'}, status=400)
        if 'visit_date' in data:
            location.visit_date = data['visit_date'] or None
        if 'notes' in data:
            location.notes = data['notes']

        # 保存修改到数据库
        location.save()

        return JsonResponse({
            'message': '地点更新成功',
            'location': location_to_dict(location)
        })

    elif request.method == 'DELETE':
        # ========== 删除地点 ==========
        # 注意：因为 Photo 模型的外键设置了 on_delete=models.CASCADE，
        # 所以删除地点时，这个地点的所有照片也会自动被删除
        location.delete()
        return JsonResponse({'message': '地点删除成功'}, status=200)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])


@csrf_exempt
def photo_list(request, location_id):
    """
    照片列表 API - 处理某个地点的照片：
    - GET: 获取某个地点的所有照片
    - POST: 给某个地点上传新照片

    URL: /api/locations/<location_id>/photos/
    """

    # 先找到对应的地点
    location = Location.objects.filter(id=location_id).first()
    if not location:
        return JsonResponse({'error': '地点不存在'}, status=404)

    if request.method == 'GET':
        # ========== 获取该地点的所有照片 ==========
        photos = location.photos.all()
        data = [
            {
                'id': photo.id,
                'image': photo.image.url,
                'description': photo.description,
                'uploaded_at': str(photo.uploaded_at),
            }
            for photo in photos
        ]
        return JsonResponse({'photos': data, 'count': len(data)})

    elif request.method == 'POST':
        # ========== 上传新照片 ==========
        # 注意：上传文件不能用 JSON 格式，前端需要用 multipart/form-data 格式提交
        # request.FILES 是 Django 专门用来获取上传文件的字典
        if 'image' not in request.FILES:
            return JsonResponse({'error': '请选择要上传的图片'}, status=400)

        # 获取上传的图片文件
        image_file = request.FILES['image']

        # 获取图片描述（从 POST 表单数据里取，不是从 JSON 里）
        description = request.POST.get('description', '').strip()

        # 创建照片对象并保存
        # Photo.objects.create() 会自动把图片文件保存到 MEDIA_ROOT 目录下
        photo = Photo.objects.create(
            location=location,
            image=image_file,
            description=description,
        )

        return JsonResponse({
            'message': '照片上传成功',
            'photo': {
                'id': photo.id,
                'image': photo.image.url,
                'description': photo.description,
                'uploaded_at': str(photo.uploaded_at),
            }
        }, status=201)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def photo_detail(request, location_id, photo_id):
    """
    单张照片 API - 删除单张照片

    URL: /api/locations/<location_id>/photos/<photo_id>/
    """

    # 先找到地点
    location = Location.objects.filter(id=location_id).first()
    if not location:
        return JsonResponse({'error': '地点不存在'}, status=404)

    # 再找到属于这个地点的照片
    # 用 location=location 过滤，确保这张照片确实属于这个地点，防止越权访问
    photo = location.photos.filter(id=photo_id).first()
    if not photo:
        return JsonResponse({'error': '照片不存在'}, status=404)

    if request.method == 'DELETE':
        # 删除照片
        # photo.delete() 会删除数据库记录，同时也会删除磁盘上的图片文件
        # 注意：Django 默认不会自动删除文件，需要手动处理，这里我们手动删除
        if photo.image:
            # 删除磁盘上的图片文件
            default_storage.delete(photo.image.name)
        # 删除数据库记录
        photo.delete()
        return JsonResponse({'message': '照片删除成功'})

    else:
        return HttpResponseNotAllowed(['DELETE'])
