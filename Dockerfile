FROM python:3.7-slim-stretch

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
# RUN ["flask", "run"]