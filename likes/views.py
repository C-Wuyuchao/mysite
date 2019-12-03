from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from likes.models import LikeRecord, LikeCount


def success_response(liked_num):
    data = {
        'status': 'Success',
        'liked_num': liked_num
    }
    return JsonResponse(data)


def fail_response(code, message):
    data = {
        'status': 'Error',
        'code': code,
        'message': message,
    }
    return JsonResponse(data)


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        # 没有登录
        code = 400
        message = '您没有登录，请登录后再点赞'
        return fail_response(code, message)
    # 获取数据
    object_id = int(request.GET.get('object_id'))
    content_type = request.GET.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(id=object_id)
    except ObjectDoesNotExist:
        code = 404
        message = '点赞对象不存在'
        return fail_response(code, message)

    is_like = request.GET.get('is_like')
    # 处理数据
    if is_like == 'true':
        # 点赞
        # 创建或获取记录
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return success_response(like_count.liked_num)
        else:
            # 已点赞  不能重复点赞
            code = 401
            message = '您已经赞过了'
            return fail_response(code, message)
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 已赞过  取消点赞
            like_record = LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()

            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return success_response(like_count.liked_num)
            else:
                # 没有点赞过 不能重复取消
                code = 404
                message = '数据错误'
                return fail_response(code, message)
        else:
            # 没有点赞过 不能重复取消
            code = 403
            message = '您没有点赞过，不能取消点赞'
            return fail_response(code, message)
