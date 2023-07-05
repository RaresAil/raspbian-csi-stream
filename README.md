# raspbian-csi-stream
low latency rpi csi camera stream using opencv, flask, libcamera-vid

### Features!

- You can open multiple browsers at the same time
- The speed of the video is very fast, almost real time
- The stream uses UDP

### Commands to run:

```bash
$ sudo apt update --fix-missing
$ sudo apt install -y libopenjp2-7-dev libhdf5-dev libatlas-base-dev python3-pip python3-h5py python3-opencv libqt5gui5 libqt5webkit5 libqt5test5
$ sudo pip3 install flask
```

### Python3 Script & libcamera-vid

- Check the app.py for the python script
- The libcamera-vid command to stream from the camera as UDP is, for fast response, do not increase the resolution, i used Module 3
```
libcamera-vid -t 0 --level 4.2 --denoise cdn_off --codec mjpeg --inline -o udp://127.0.0.1:5800 -n --segment 1 -q 80 --width 854 --height 480
```

### Systemd Services

#### For libcamera

```
sudo nano /lib/systemd/system/pi-vid.service
```

Contents

```service
[Unit]
Description=The Pi camera stream in UDP
After=network.target

[Service]
User=pi
Type=simple
ExecStart=/usr/bin/libcamera-vid -t 0 --level 4.2 --denoise cdn_off --codec mjpeg --inline -o udp://127.0.0.1:5800 -n --segment 1 -q 80 --width 854 --height 480
Restart=always

[Install]
WantedBy=multi-user.target
```

To start the service and enable it to start at boot
```
$ sudo systemctl start pi-vid
$ sudo systemctl enable pi-vid
```

#### For python script

```
sudo nano /lib/systemd/system/pi-vid-stream.service
```

Contents, the WorkingDirectory has to be set inside the folder with app.py

```service
[Unit]
Description=The Pi camera stream in HTTP
Requires=pi-vid.service
After=pi-vid.service

[Service]
User=pi
Type=simple
WorkingDirectory=/home/pi/raspbian-csi-stream
ExecStart=/usr/bin/python3 ./app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

To start the service and enable it to start at boot
```
$ sudo systemctl start pi-vid-stream
$ sudo systemctl enable pi-vid-stream
```

### To view the stream create a html file with the following data and open it

`192.168.x.x` has to be the ip of the rpi

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <img
      id="bg"
      src="http://192.168.x.x:5700/video_feed"
      style="width: 88%"
    />
  </body>
</html>
```
