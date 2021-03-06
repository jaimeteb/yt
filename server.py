import os
import json
import uuid
import glob
import base64
import logging

from youtube_dl import YoutubeDL
from flask import Flask, render_template, request
from urllib import request as urlreq

logging.basicConfig(level=logging.INFO)

app = Flask(
    __name__,
    template_folder="templates"
)

MEDIA_PATH = 'media/'


def thumb64(url):
    urlreq.urlretrieve(url, "/app/media/thumb.jpg")
    with open("/app/media/thumb.jpg", "rb") as image:
        raw = image.read()

    os.remove("/app/media/thumb.jpg")

    b64 = base64.b64encode(raw)
    uri = b64.decode("utf-8")
    return uri


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    data = request.get_json()
    url = data["url"]
    ytid = url[url.find("=")+1:]
    # playid = str(uuid.uuid4())[-8:]

    config = {
        "outtmpl": "/app/media/%(id)s.%(ext)s",
        "verbose": True
    }

    with YoutubeDL(config) as ytdl:
        ytdl.download([url])
        info_dict = ytdl.extract_info(url, download=False)
        logging.info("INFO DICT:\n")
        logging.info(json.dumps(info_dict, indent=4))
        # video_url = info_dict.get("url", None)
        # video_id = info_dict.get("id", None)
        video_title = info_dict.get('title', None)

    logging.info("VIDEO ID: " + ytid)

    with open(f"media/{ytid}.mp4", "rb") as video:
        raw = video.read()

    os.remove(f"media/{ytid}.mp4")

    b64 = base64.b64encode(raw)
    uri = b64.decode("utf-8")

    return json.dumps({
        "uri": uri,
        "title": video_title
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
        "writeinfojson": True,
        "ignoreerrors": True,
        "verbose": True
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
            "thumb": thumb64(thumb),
            "title": title,
            "url": url
        })

        os.remove(filename)


    logging.info("SEARCH SUCCESSFUL")

    html = render_template(
        "results.html",
        results = [(r["thumb"], r["title"], r["url"]) for r in results]
    )

    return json.dumps({
        "results": html
    })



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5000',
        threaded=True
    )
