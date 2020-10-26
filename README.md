# FFmpeg-RTSP-HLS-View

Sample web application which allows to consume RTSP streams at the backend and provides HLS output for the client into the browser.  

## Build and run in Docker
```
docker build --no-cache -t "ffmpeg-rtsp-hls:0.0.1" .
docker volume create hls-out
docker run --rm -v hls-out:/opt/ffmpeg-rtsp-hls/hls-out -p 8080:8080 "ffmpeg-rtsp-hls:0.0.1"
```