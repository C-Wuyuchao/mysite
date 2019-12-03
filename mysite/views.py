import datetime

from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from blog.models import Blog
from read_statistics.utils import get_sevdays_read_data, get_today_hot_data, get_yesterday_hot_data


def get_7_days_hot_blogs():
    today = timezone.now().date()
    before_7_days = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
        .filter(read_details__date__lt=today, read_details__date__gt=before_7_days)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')[:7]
    return blogs


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_num_list, day_list = get_sevdays_read_data(blog_content_type)
    hot_today = get_today_hot_data(blog_content_type)
    hot_yesterday = get_yesterday_hot_data(blog_content_type)

    # 获取七天热门补课的缓存数据
    hot_senven_blogs = cache.get('get_7_days_hot_blogs')
    if hot_senven_blogs is None:
        hot_senven_blogs = get_7_days_hot_blogs()
        cache.set('get_7_days_hot_blogs', hot_senven_blogs, 3600)
        print('存入缓存')
    else:
        print('使用缓存')
    context = {
        'read_nums': read_num_list,
        'day_list': day_list,
        'hot_today': hot_today,
        'hot_yesterday': hot_yesterday,
        'hot_sevendays': hot_senven_blogs,
    }
    return render(request, 'home.html', context)


