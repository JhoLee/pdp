# Dockerfiles

FROM ubuntu:18.04
MAINTAINER Jho Lee "jho.lee@kakao.com"


ENV CONDA="/root/miniconda3"
ENV PATH="${CONDA}/bin:${PATH}"
ARG PATH="${CONDA}/bin:${PATH}"

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y wget && \
       rm -rf /var/lib/apt/lists/*
WORKDIR /app

# copy sources
COPY ./api /app/api
COPY ./models /app/models

# install conda
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -p /root/miniconda3 -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN source ~/.bashrc \
    && conda update -y conda \
    && conda init bash \
    && source ~/.bashrc

# conda environments
RUN conda install \
        opencv \
        django \
        Pillow \
 && conda clean -afy \
 && pip install --no-cache-dir \
        Celery


# copy sources
COPY pdf_front /app/pdf_front

WORKDIR /app/pdf_front

# Develop server
RUN python gen_secret_key.py \
 && python manage.py runserver
