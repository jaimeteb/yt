FROM python:3.7

WORKDIR /app
ADD . /app

RUN pip install flask youtube-dl

EXPOSE 5000

CMD ["python", "server.py"]
