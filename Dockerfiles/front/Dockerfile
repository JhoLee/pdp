# Dockerfiles

FROM ubuntu:18.04
MAINTAINER Jho Lee "jho.lee@kakao.com"

ENV PYTHONBUFFERED 1


ENV CONDA="/root/miniconda3"
ENV PATH="${CONDA}/bin:${PATH}"
ARG PATH="${CONDA}/bin:${PATH}"

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y wget && \
       rm -rf /var/lib/apt/lists/*

# copy sources
COPY ./api /app

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
 && conda clean -afy
RUN pip install --no-cache-dir \
        Celery \
        bcrypt


# copy sources
COPY front /app

WORKDIR /app

CMD ["bash", "-c", "./entry_point.sh"]
#CMD ["python", "manage.py", "runserver", "0:8000"]
