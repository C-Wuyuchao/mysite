import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistic_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.id)
    if not request.COOKIES.get(key):
        # 总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)
        readnum.read_num += 1
        readnum.save()

        #  当天阅读数+1
        date = timezone.now().date()
        read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return key


def get_sevdays_read_data(content_type):
    today = timezone.now().date()
    read_num_list = []
    day_list = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        day_list.append(date.strftime("%m/%d"))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_num_list.append(result['read_num_sum'] or 0)
    return read_num_list, day_list


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')[:7]
    return read_details


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')[:7]
    return read_details

