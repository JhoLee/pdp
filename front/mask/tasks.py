from __future__ import absolute_import, unicode_literals

from time import sleep

from celery import shared_task
from .models import Post


@shared_task
def sleepy(duration):
    print('hi')
    sleep(duration)
    return None


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_posts():
    return Post.objects.count()


@shared_task
def retitle_post(post_id, title):
    p = Post.object.get(id=post_id)
    p.title = title
    p.save()
