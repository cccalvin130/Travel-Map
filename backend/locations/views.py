import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Location, Photo


def location_to_dict(location):
    """
    把一个 Location 对象转换成字典
    因为 Django 的对象不能直接转成 JSON 返回给前端，
    所以要手动把每个字段取出来，组成字典
    """
    return {
        'id': location.id,
        'name': location.name,
        'country': location.country,
        'city': location.city,
        'latitude': float(location.latitude),
        'longitude': float(location.longitude),
        'visit_date': str(location.visit_date) if location.visit_date else None,
        'notes': location.notes,
        'photos': [
            {
                'id': photo.id,
                'image': photo.image.url,
                'description': photo.description,
            }
            for photo in location.photos.all()
        ]
    }


@csrf_exempt
def location_list(request):
    """
    地点列表接口
    - GET: 获取所有地点
    - POST: 创建新地点
    网址: /api/locations/
    """

    if request.method == 'GET':
        # 从数据库取出所有地点
        locations = Location.objects.all()
        # 把每个地点转成字典，组成列表
        result = [location_to_dict(loc) for loc in locations]
        # 返回 JSON 给前端
        return JsonResponse({'locations': result})

    elif request.method == 'POST':
        # 读取前端发来的 JSON 数据，转成 Python 字典
        data = json.loads(request.body)

        # 从字典里取出每个字段的值
        name = data['name']
        country = data['country']
        city = data['city']
        latitude = data['latitude']
        longitude = data['longitude']
        visit_date = data.get('visit_date')  # get 表示这个字段可以没有
        notes = data.get('notes', '')         # 没有的话默认是空字符串

        # 创建新地点并保存到数据库
        new_location = Location.objects.create(
            name=name,
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            visit_date=visit_date,
            notes=notes,
        )

        # 返回创建成功的消息和新地点的数据
        return JsonResponse({
            'message': '创建成功',
            'location': location_to_dict(new_location),
        })


@csrf_exempt
def location_detail(request, location_id):
    """
    单个地点接口
    - GET: 获取一个地点的详情
    - PUT: 修改地点信息
    - DELETE: 删除地点
    网址: /api/locations/地点id/
    """

    # 根据 id 从数据库找到这个地点
    # 如果找不到就返回 None
    location = Location.objects.filter(id=location_id).first()

    # 如果找不到，返回错误
    if not location:
        return JsonResponse({'error': '地点不存在'}, status=404)

    if request.method == 'GET':
        # 返回这个地点的数据
        return JsonResponse({'location': location_to_dict(location)})

    elif request.method == 'PUT':
        # 读取前端发来的 JSON 数据
        data = json.loads(request.body)

        # 如果前端传了这个字段，就更新，否则保持原来的值
        if 'name' in data:
            location.name = data['name']
        if 'country' in data:
            location.country = data['country']
        if 'city' in data:
            location.city = data['city']
        if 'latitude' in data:
            location.latitude = data['latitude']
        if 'longitude' in data:
            location.longitude = data['longitude']
        if 'visit_date' in data:
            location.visit_date = data['visit_date']
        if 'notes' in data:
            location.notes = data['notes']

        # 保存修改到数据库
        location.save()

        return JsonResponse({
            'message': '修改成功',
            'location': location_to_dict(location),
        })

    elif request.method == 'DELETE':
        # 删除这个地点
        # 注意：因为 Photo 的外键设置了 CASCADE，
        # 所以删除地点时，这个地点的所有照片也会自动删除
        location.delete()
        return JsonResponse({'message': '删除成功'})


@csrf_exempt
def photo_list(request, location_id):
    """
    照片列表接口
    - GET: 获取某个地点的所有照片
    - POST: 给某个地点上传新照片
    网址: /api/locations/地点id/photos/
    """

    # 先找到对应的地点
    location = Location.objects.filter(id=location_id).first()
    if not location:
        return JsonResponse({'error': '地点不存在'}, status=404)

    if request.method == 'GET':
        # 取出这个地点的所有照片
        photos = location.photos.all()
        # 转成字典列表
        result = [
            {
                'id': photo.id,
                'image': photo.image.url,
                'description': photo.description,
            }
            for photo in photos
        ]
        return JsonResponse({'photos': result})

    elif request.method == 'POST':
        # 从请求中取出上传的图片文件
        # 注意：上传图片不能用 JSON，要用表单格式(multipart/form-data)
        image_file = request.FILES['image']
        # 取出图片描述（可以没有）
        description = request.POST.get('description', '')

        # 创建新照片并保存
        new_photo = Photo.objects.create(
            location=location,
            image=image_file,
            description=description,
        )

        return JsonResponse({
            'message': '照片上传成功',
            'photo': {
                'id': new_photo.id,
                'image': new_photo.image.url,
                'description': new_photo.description,
            },
        })


@csrf_exempt
def photo_detail(request, location_id, photo_id):
    """
    单张照片接口
    - DELETE: 删除一张照片
    网址: /api/locations/地点id/photos/照片id/
    """

    # 先找到地点
    location = Location.objects.filter(id=location_id).first()
    if not location:
        return JsonResponse({'error': '地点不存在'}, status=404)

    # 再找到属于这个地点的照片
    photo = location.photos.filter(id=photo_id).first()
    if not photo:
        return JsonResponse({'error': '照片不存在'}, status=404)

    if request.method == 'DELETE':
        # 删除照片
        photo.delete()
        return JsonResponse({'message': '照片删除成功'})
