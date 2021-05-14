FROM python:latest
RUN pip install --upgrade pip
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
