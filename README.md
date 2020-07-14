# YT
YouTube videos as mp4 in a simple web application.

This app was developed as a way to practice Flask, Bootstrap and Docker. It uses the [YouTube DL](https://github.com/ytdl-org/youtube-dl) library to search and download YouTube videos, that are embedded in an HTML video player using base64 encoding.

~~This application was never installed in a virtual machine in order to watch YouTube videos in a network where the site is blocked.~~

## Requirements

* Docker

## Usage

1. Clone the project and ```cd``` into it.
2. Use ```docker build -t yt .``` to build the image.
3. Use ```docker run -p 5000:5000 yt``` to run the app.
4. Go to **localhost:5000** on your web browser.

  ![Rick Astley](/media/rick.PNG)

  On the left side of the page you'll be able to search for videos based on a query string. A maximum of 5 results will be shown, consisting of their titles, thumbnails and URLs.

  Click on any of the results to load the video. After loading is finished, you'll se the video player on the right side.

  Also, if you have a YouTube video URL you can paste it on the right input field and press Play.
