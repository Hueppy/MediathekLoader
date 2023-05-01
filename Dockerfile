FROM alpine:latest

RUN apk update && \
    apk add ffmpeg python3 py3-pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py main.py

CMD ["python", "./main.py"]
