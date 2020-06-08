import os

import cv2
import magic
import numpy as np
from django.core.files.base import ContentFile
from api.celery import app
from api.settings import BASE_DIR

from .models import MaskRequest, MaskResult
from .seg_models.torchmodel import TorchModel
from .utils import combined_masking, check_file_type

models = ('deeplabv3_resnet101', 'fcn_resnet101')


@app.task(bind=True)
def mask_image(self, mask_request_id):
    try:
        # update the task id on the mask_request for future monitoring
        mask_request = MaskRequest.objects.get(id=mask_request_id)
        mask_request.task_id = self.request.id
        mask_request.maskresult.status = MaskResult.Status.PROCESSING
        mask_request.save()

        # loading model architecture
        self.update_state(state='Loading models', meta={'progress': 0})
        torch_model = TorchModel()

        ## pre-processing the image
        self.update_state(state='Pre-processing the image', meta={'progress': 30})
        file_path = os.path.join(BASE_DIR, 'media', str(mask_request.file))
        torch_model.frame = file_path
        torch_model.preprocess_image()

        ## finding the face
        self.update_state(state='Finding the face', meta={'progress': 50})
        torch_model.predict()
        mask = torch_model.mask

        ## masking the face
        self.update_state(state='Masking the face', meta={'progress': 90})
        img = torch_model.frame
        result = combined_masking(img, mask)

        # Save
        # print(result.shape)
        _, out_img = cv2.imencode('.jpg', np.asarray(result))
        out_img = out_img.tobytes()
        out_file = ContentFile(out_img)
        out_path = file_path.replace('/original/', '/mask/')
        mask_request.maskresult.result_file.save(out_path, out_file)
        mask_request.maskresult.status = MaskResult.Status.FINISH
        mask_request.save()
        e = 1

    except Exception as e:
        mask_request.maskresult.status = MaskResult.Status.ERROR
        mask_request.save()
        print()
        print(str(e))

    finally:
        # finish
        self.update_state(state='Finished', meta={'progress': 100})


@app.task(bind=True)
def mask_video(self, mask_request_id):
    try:
        # update the task id on the mask_request for future monitoring
        mask_request = MaskRequest.objects.get(id=mask_request_id)
        mask_request.task_id = self.request.id
        mask_request.maskresult.status = MaskResult.Status.PROCESSING
        mask_request.save()

        # loading model architecture
        self.update_state(state='Loading models', meta={'progress': 0})
        torch_model = TorchModel()

        # find the faces form the video
        self.update_state(state='Finding faces from the video and masking', meta={'progress': 30})
        file_path = os.path.join(BASE_DIR, 'media', str(mask_request.file))

        cap = cv2.VideoCapture(file_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

        out_path = file_path.replace('/original/', '/result/')
        writer = cv2.VideoWriter(out_path,
                                 fourcc,
                                 fps,
                                 (width, height))
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w, _ = frame.shape
                torch_model.frame = frame
                torch_model.preprocess_image()

                torch_model.predict()
                mask = torch_model.mask

                # masking the face
                writer.write(combined_masking(frame, mask))
        writer.release()
        # Save
        with open(out_path, 'rb') as f:
            mask_request.maskresult.result_file.save(out_path, ContentFile(f))
        mask_request.maskresult.status = MaskResult.Status.FINISH
        mask_request.save()
        e = 1

    except Exception as e:
        mask_request.maskresult.status = MaskResult.Status.ERROR
        mask_request.save()
        print()
        print(str(e))

    finally:
        # finish
        self.update_state(state='Finished', meta={'progress': 100})
