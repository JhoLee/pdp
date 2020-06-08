# Dockerfiles

FROM ubuntu:16.04
MAINTAINER Jho Lee "jho.lee@kakao.com"


ENV CONDA="/root/miniconda3"
ENV PATH="${CONDA}/bin:${PATH}"
ARG PATH="${CONDA}/bin:${PATH}"

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y \
        wget \
        libmagic1 \
        && \
    rm -rf /var/lib/apt/lists/*

# copy sources
COPY ./api /app

# install conda
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -p /root/miniconda3 -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

#RUN curl -O -J -L \
#    https://bit.ly/pytorch_mrcnn_coco_pth \
# && mv mask_rcnn_coco.pth models

RUN source ~/.bashrc \
    && conda update -y conda \
    && conda init bash \
    && source ~/.bashrc

# conda environments
RUN conda install -c pytorch \
        pytorch \
        torchvision \
        cudatoolkit \
        cudnn \
 && conda install \
        opencv \
        Pillow \
        tqdm \
        django \
        Celery \
        Cython \
        matplotlib \
 && conda clean -afy \
 && pip install --no-cache-dir \
        segmentation-models-pytorch==0.1.0 \
        djangorestframework==3.11.0 \
        markdown==3.2.2 \
        django-filter==2.2.0 \
        python-magic==0.4.18


WORKDIR /app

RUN ls -al

CMD ["bash", "-c", "./entry_point.sh"]
