from django.contrib.auth.hashers import is_password_usable, make_password
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class Status(models.TextChoices):
        STAND_BY = 'SB', _('StandBy')
        PROCESSING = 'PR', _('Processing')
        FINISH = 'FN', _('Finish')
        ERROR = 'ER', _('Error')
        DELETE_USER = 'DU', _('Deleted by User')
        EXPIRED = 'EX', _('Expired')

    title = models.CharField(max_length=30)
    author = models.CharField(max_length=10)
    password = models.CharField(max_length=60)
    image = models.ImageField(default=None, upload_to='origin/%Y/%m/%d', null=True)
    method = models.CharField
    result_image = models.ImageField(blank=True, upload_to='mask/%Y/%m/%d')
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.STAND_BY
    )
    reg_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        mod_date = self.mod_date.strftime("%Y%m%d_%H:%M:%S") if self.mod_date is not None else None
        mod_date = "({})".format(mod_date) if mod_date is not None else ""
        name = "{title} - {author} - {status}{mod_date} - {reg_date}".format(
            title=self.title,
            author=self.author,
            status=self.status,
            reg_date=self.reg_date.strftime("%Y%m%d_%H:%M:%S"),
            mod_date=mod_date
        )
        return name


# @receiver(pre_save, sender=Request)
# def password_hashing(instance, **kwargs):
#     if not is_password_usable(instance.password):
#         instance.password = make_password(instance.password)
