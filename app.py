import cv2
import numpy
import time
import threading
from flask import Flask, render_template, Response, stream_with_context, request

app = Flask(__name__)

video = None
frames = None
thread_lock = threading.Lock()
stop_flag = threading.Event()

def read_frames():
    global video, frames, stop_flag
    while not stop_flag.is_set():
        if not video.isOpened():
            continue
        ret, frame = video.read()
        if not ret:
            print('Failed to read stream')
            continue
        with thread_lock:
            frames = frame

def release_video():
    global video
    if video is not None:
        print("Release video")
        video.release()

def video_stream():
    while True:
        with thread_lock:
            frame = frames
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpeg',frame)
        if not ret:
            print('Failed to encode frame')
            continue
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    video = cv2.VideoCapture('udp://127.0.0.1:5800?fifo_size=5000000')

    frame_thread = threading.Thread(target=read_frames, daemon=True)
    frame_thread.start()

    app.run(host='0.0.0.0', port='5700', debug=False)

    print("Stopping frame_thread")
    stop_flag.set()
    frame_thread.join()

    release_video()
