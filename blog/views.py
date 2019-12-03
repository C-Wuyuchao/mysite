from django.shortcuts import render, get_object_or_404
from blog.models import Blog, BlogType
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings

from user.forms import LoginForm
from read_statistics.utils import read_statistic_once_read


def blog_paginator(request, blogs_all_list):
    """
    实现分页，
    :param request:
    :param blogs_all_list: 当前列表集合
    :return:
    """
    paginator = Paginator(blogs_all_list, settings.BLOG_NUM_EACH_PAGE)
    page_num = request.GET.get('page', 1)  # 获取页码参数， 默认为1
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取前后页码各两页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标签
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类对应数量
    blogs_types_list = BlogType.objects.annotate(blog_count=Count('blog'))
    """blogs_types_list = []
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blogs_types_list.append(blog_type)
        """
    # 获取博客日期分类对应数量
    blog_dates_dict = {}
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = {
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'page_range': page_range,
        'blog_types': blogs_types_list,
        'blog_dates': blog_dates_dict,
    }
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = blog_paginator(request, blogs_all_list)
    return render(request, 'blog_list.html', context)


def blogs_with_type(request, blog_with_type):
    blog_type = get_object_or_404(BlogType, id=blog_with_type)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = blog_paginator(request, blogs_all_list)
    return render(request, 'blogs_with_type.html', context)


def blogs_with_date(request, year, month):

    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = blog_paginator(request, blogs_all_list)
    return render(request, 'blog_with_date.html', context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # 获取key
    read_cookie_key = read_statistic_once_read(request, blog)

    context = {
        'pre_blog': Blog.objects.filter(created_time__gt=blog.created_time).last(),
        'blog': get_object_or_404(Blog, id=blog_id),
        'next_blog': Blog.objects.filter(created_time__lt=blog.created_time).first(),
        'login_form': LoginForm(),
    }
    response = render(request, 'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 阅读标记
    return response
