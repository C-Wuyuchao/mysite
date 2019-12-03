from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.simple_tag()
def get_comment_count_tag(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_count = Comment.objects.filter(content_type=content_type, object_id=obj.id).count()
    return comment_count


@register.simple_tag()
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_form = CommentForm(initial={
        'object_id': obj.id, 'content_type': content_type.model, 'reply_comment_id': 0}, )
    return comment_form


@register.simple_tag()
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment = Comment.objects.filter(content_type=content_type, object_id=obj.id, parent=None).order_by('-comment_time')
    return comment
