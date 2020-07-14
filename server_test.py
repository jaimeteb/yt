import os
import json
import uuid
import glob
import logging

from youtube_dl import YoutubeDL

query = "Rick Astley"
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

logging.info(results)
