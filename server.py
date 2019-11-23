import os
import json
import uuid
import glob
import base64
import logging

from youtube_dl import YoutubeDL
from flask import Flask, render_template, request

logging.basicConfig(level=logging.INFO)

app = Flask(
    __name__,
    template_folder="templates"
)

MEDIA_PATH = 'media/'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    data = request.get_json()
    url = data["url"]
    ytid = url[url.find("=")+1:]

    config = {
        "outtmpl": "/app/media/%(id)s.%(ext)s"
    }

    with YoutubeDL(config) as ytdl:
        ytdl.download([url])

    logging.info("VIDEO ID: " + ytid)

    with open(f"media/{ytid}.mp4", "rb") as video:
        raw = video.read()

    os.remove(f"media/{ytid}.mp4")

    b64 = base64.b64encode(raw)
    uri = b64.decode("utf-8")

    return json.dumps({
        "uri": uri
    })


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data["query"]
    searchid = str(uuid.uuid4())[-8:]

    search_config = {
        "default_search": "ytsearch5",
        "outtmpl": f"/app/json/{searchid}_%(id)s",
        "skip_download": True,
        "writeinfojson": True
    }

    with YoutubeDL(search_config) as ytdl:
        ytdl.download([query])

    results = []
    for filename in glob.glob(f"/app/json/{searchid}_*.info.json"):
        with open(filename, "r") as file:
            info = json.load(file)

        thumb = info["thumbnail"]
        title = info["title"]
        url = info["webpage_url"]

        results.append({
            "thumb": thumb,
            "title": title,
            "url": url
        })

    logging.info("SEARCH SUCCESSFUL")
    return json.dumps({
        "results": results
    })



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5000',
        threaded=True
    )
