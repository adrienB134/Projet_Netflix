FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update&
RUN apt-get install nano unzip
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt ./dependencies/requirements.txt
RUN pip install -r ./dependencies/requirements.txt

COPY main.py /home/app


CMD gunicorn app:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker