import os
import uu
import json
import base64
import logging
import youtube_dl
from flask import Flask, send_file, make_response, render_template, request, redirect, url_for

logging.basicConfig(level=logging.INFO)

app = Flask(
    __name__,
    template_folder="templates"
)
MEDIA_PATH = 'media/'

YTDL = youtube_dl.YoutubeDL({'outtmpl': '/app/media/%(id)s.%(ext)s'})

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    url = data["url"]
    ytid = url[url.find("=")+1:]

    with YTDL:
        YTDL.download([url])

    logging.info("VIDEO ID: " + ytid)

    with open(f"media/{ytid}.mp4", "rb") as video:
        raw = video.read()

    b64 = base64.b64encode(raw)
    uri = b64.decode("utf-8")

    return json.dumps({
        "uri": uri
    })


@app.route('/media/<vid_name>')
def serve_video(vid_name):
    vid_path = os.path.join(MEDIA_PATH, vid_name)
    resp = make_response(send_file(vid_path, 'video/mp4'))
    resp.headers['Content-Disposition'] = 'inline'
    return resp


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5000',
        threaded=True
    )
