import os
import youtube_dl
from flask import Flask, send_file, make_response, render_template, request, redirect, url_for


app = Flask(
    __name__,
    template_folder="templates"
)
MEDIA_PATH = './media/'

YTDL = youtube_dl.YoutubeDL({'outtmpl': './media/%(id)s.%(ext)s'})

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    url = data["url"]
    ytid = url[url.find("=")+1:-1]

    with YTDL:
        YTDL.download([url])

    return redirect(url_for(ytid + ".mp4"))


@app.route('/<vid_name>')
def serve_video(vid_name):
    vid_path = os.path.join(MEDIA_PATH, vid_name)
    resp = make_response(send_file(vid_path, 'video/mp4'))
    resp.headers['Content-Disposition'] = 'inline'
    return resp


if __name__ == '__main__':
    app.run()
