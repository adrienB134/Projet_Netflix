FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt ./dependencies/requirements.txt
RUN pip install -r ./dependencies/requirements.txt
RUN conda install -c conda-forge scikit-surprise

COPY app.py /home/app

ENV MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

CMD gunicorn app:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker