---
name: linux-webcam
description: Capture images and video from webcam on Linux using fswebcam or ffmpeg. Take snapshots, record video clips, and stream from camera. Use when a user asks FRIDAY to take a photo, capture webcam, or record video on Linux.
homepage: https://github.com/fsphil/fswebcam
metadata: {"friday":{"emoji":"📷","os":["linux"],"requires":{"bins":["fswebcam"]},"install":[{"id":"apt-fswebcam","kind":"apt","package":"fswebcam","bins":["fswebcam"],"label":"Install fswebcam via apt"}]}}
---

# Linux Webcam CLI

Use `fswebcam` or `ffmpeg` to capture images and video from webcam. This is a Linux alternative to macOS camsnap.

## Setup
Install fswebcam:
```bash
sudo apt-get install -y fswebcam
```

Install ffmpeg (for video):
```bash
sudo apt-get install -y ffmpeg
```

Check available cameras:
```bash
ls -la /dev/video*
```

## Capture Photos with fswebcam

### Basic snapshot
```bash
fswebcam ~/Pictures/webcam.jpg
```

### Specify device
```bash
fswebcam -d /dev/video0 ~/Pictures/webcam.jpg
```

### Set resolution
```bash
fswebcam -r 1280x720 ~/Pictures/webcam-hd.jpg
```

### High resolution
```bash
fswebcam -r 1920x1080 ~/Pictures/webcam-fhd.jpg
```

### No banner (clean image)
```bash
fswebcam --no-banner ~/Pictures/webcam.jpg
```

### With delay (let camera adjust)
```bash
fswebcam -D 2 --no-banner ~/Pictures/webcam.jpg
```

### Skip initial frames (better exposure)
```bash
fswebcam -S 10 --no-banner ~/Pictures/webcam.jpg
```

### Multiple frames averaged (reduces noise)
```bash
fswebcam -F 5 --no-banner ~/Pictures/webcam.jpg
```

### Best quality shot
```bash
fswebcam -r 1920x1080 -D 2 -S 20 -F 5 --no-banner ~/Pictures/webcam.jpg
```

### PNG format
```bash
fswebcam --png 9 ~/Pictures/webcam.png
```

### With timestamp
```bash
fswebcam --timestamp "%Y-%m-%d %H:%M:%S" ~/Pictures/webcam.jpg
```

## Record Video with ffmpeg

### Record 10 seconds of video
```bash
ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i /dev/video0 -t 10 ~/Videos/webcam.mp4
```

### Record with audio
```bash
ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i /dev/video0 \
       -f pulse -i default \
       -c:v libx264 -preset ultrafast -c:a aac \
       -t 10 ~/Videos/webcam-audio.mp4
```

### Record until stopped (Ctrl+C)
```bash
ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i /dev/video0 -c:v libx264 -preset ultrafast ~/Videos/webcam.mp4
```

### Preview webcam (without recording)
```bash
ffplay -f v4l2 -framerate 30 -video_size 640x480 /dev/video0
```

### Lower quality for smaller file
```bash
ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i /dev/video0 -c:v libx264 -crf 28 -t 30 ~/Videos/webcam.mp4
```

## Timelapse

### Capture timelapse frames
```bash
mkdir -p ~/Pictures/timelapse
for i in $(seq 1 100); do
  fswebcam -r 1280x720 --no-banner ~/Pictures/timelapse/frame-$(printf "%04d" $i).jpg
  sleep 5
done
```

### Convert frames to video
```bash
ffmpeg -framerate 10 -pattern_type glob -i '~/Pictures/timelapse/*.jpg' -c:v libx264 -pix_fmt yuv420p ~/Videos/timelapse.mp4
```

## Advanced

### List camera capabilities
```bash
v4l2-ctl --list-formats-ext -d /dev/video0
```

### Adjust camera settings
```bash
v4l2-ctl -d /dev/video0 --set-ctrl brightness=128
v4l2-ctl -d /dev/video0 --set-ctrl contrast=128
```

### List available controls
```bash
v4l2-ctl -d /dev/video0 --list-ctrls
```

## Cheese (GUI Alternative)

### Install Cheese
```bash
sudo apt-get install -y cheese
```

### Launch
```bash
cheese
```

## Notes
- Linux-only (alternative to macOS camsnap).
- Default camera is usually `/dev/video0`.
- Use `v4l2-ctl` for advanced camera control.
- `fswebcam` skips first few frames by default for better exposure.
- Add user to `video` group if permission denied: `sudo usermod -aG video $USER`
