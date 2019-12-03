from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse

from .models import Comment
from .forms import CommentForm


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        # 保存评论
        parent = comment_form.cleaned_data['parent']
        if parent:
            if parent.root:
                comment.root = parent.root
            else:
                comment.root = parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # 发送邮件通知
        comment.send_mail()
        data = {
            'status': 'SUCCESS',
            'username': comment.user.username,
            'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'text': comment.text,
            'content_type': ContentType.objects.get_for_model(comment).model
        }
        if parent:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['id'] = comment.id
        # data['root_id'] = comment.root.pk if not comment.root is None else ''
        if comment.root:
            data['root_id'] = comment.root.id
        else:
            data['root_id'] = ''
    else:
        data = {
            'status': 'error',
            'message': list(comment_form.errors.values())[0][0],
        }
    return JsonResponse(data)


