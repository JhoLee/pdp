import os

import magic
from celery import chain
from celery.backends.database import TaskSet
from rest_framework import serializers

from .models import MaskRequest, MaskResult
from .tasks import mask_image, mask_video
from .utils import check_file_type
from api.settings import BASE_DIR


class MaskRequestSerializer(serializers.ModelSerializer):
    result_file = serializers.ImageField(source='maskresult.result_file', read_only=True)
    status = serializers.CharField(source='maskresult.status', read_only=True)

    class Meta:
        model = MaskRequest
        fields = ("id", "author", "file", "reg_date", "result_file", "status")

    def create(self, validated_data):
        author = validated_data.get('author')
        file = validated_data.get('file')
        reg_date = validated_data.get('reg_date')
        mask_request = MaskRequest.objects.create(
            author=author,
            file=file,
            reg_date=reg_date
        )
        file_path = os.path.join(BASE_DIR, 'media', str(mask_request.file))
        # if os.path.isdir(file_path):
        mimetype = magic.from_file(file_path, mime=True).split('/')[0]
        if mimetype == 'image':
            mask_image.delay(mask_request.id)
        elif mimetype == 'video':
            mask_video.delay(mask_request.id)
        else:
            mask_request.maskresult.status = MaskResult.Status.ERROR



        return mask_request


class MaskResultSerializer(serializers.ModelSerializer):
    request_file = serializers.ImageField(source='request.file', read_only=True)

    class Meta:
        model = MaskResult
        fields = ('status', 'request', 'request_file', 'result_file', 'mod_date')
