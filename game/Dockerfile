FROM python:3.6.1

RUN apt-get update && \
    apt-get install libzmq3-dev -yqq

ADD . /

RUN pip install -r requirements.txt

CMD ["python", "/app.py"]
