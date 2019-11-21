FROM python:3.7

WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /app

EXPOSE 5000

ENTRYPOINT  ["gunicorn"]
CMD ["-c", "gunicorn.py", "server:app"]
