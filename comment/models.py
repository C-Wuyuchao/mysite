import threading
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def send_mail(self):
        # 发送邮件通知
        if self.parent is None:
            # 回复博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复了你评论'
            email = self.reply_to.email
        if email != '':
            context = {
                'comment_text': self.text,
                'url': self.content_object.get_url(),
            }
            message = render_to_string('send_mail.html', context)
            send_mail = SendEmail(subject, message, email)

            # 启动线程
            send_mail.start()
            # 阻塞主线程，等待线程完成
            send_mail.join()

    class Meta:
        ordering = ['comment_time']


class SendEmail(threading.Thread):
    # 异步发送邮件

    def __init__(self, subject, message, email, fail_silently=False):
        super(SendEmail, self).__init__()
        self.subject = subject
        self.message = message
        self.email = email
        self.fail_silently = fail_silently


    def run(self):
        # threadLock = threading.Lock()  # 创建线程锁
        # threadLock.acquire()  # 获取线程锁
        send_mail(self.subject, self.message,
                  settings.EMAIL_HOST_USER,
                  [self.email],
                  self.fail_silently,
                  html_message=self.message
                  )
        # threadLock.release()  # 释放线程锁