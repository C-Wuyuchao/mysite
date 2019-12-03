from django.urls import path

from blog import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path(r'<int:blog_id>', views.blog_detail, name='blog_detail'),
    path(r'type/<int:blog_with_type>', views.blogs_with_type, name='blogs_with_type'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date')
]