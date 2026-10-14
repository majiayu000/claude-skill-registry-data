---
name: linux-screenshot
description: Capture screenshots on Linux using scrot, gnome-screenshot, or maim. Take full screen, window, or region screenshots. Use when a user asks FRIDAY to take a screenshot on Linux.
homepage: https://github.com/resber/scrot
metadata: {"friday":{"emoji":"📸","os":["linux"],"requires":{"bins":["scrot"]},"install":[{"id":"apt-scrot","kind":"apt","package":"scrot","bins":["scrot"],"label":"Install scrot via apt"}]}}
---

# Linux Screenshot CLI

Use `scrot` or `gnome-screenshot` to capture screenshots on Linux. This is a Linux alternative to macOS Peekaboo.

## Setup
Install scrot (recommended):
```bash
sudo apt-get install -y scrot
```

Or install gnome-screenshot:
```bash
sudo apt-get install -y gnome-screenshot
```

Or install maim (more features):
```bash
sudo apt-get install -y maim slop
```

## Capture Screenshots with scrot

### Full screen
```bash
scrot ~/Pictures/screenshot-%Y%m%d-%H%M%S.png
```

### Full screen with delay (3 seconds)
```bash
scrot -d 3 ~/Pictures/screenshot-%Y%m%d-%H%M%S.png
```

### Select region/window interactively
```bash
scrot -s ~/Pictures/screenshot-%Y%m%d-%H%M%S.png
```

### Current focused window
```bash
scrot -u ~/Pictures/window-%Y%m%d-%H%M%S.png
```

### Include window border
```bash
scrot -ub ~/Pictures/window-%Y%m%d-%H%M%S.png
```

### Capture and copy to clipboard
```bash
scrot -s - | xclip -selection clipboard -t image/png
```

### Set quality (JPEG)
```bash
scrot -q 90 ~/Pictures/screenshot.jpg
```

## Capture Screenshots with gnome-screenshot

### Full screen
```bash
gnome-screenshot -f ~/Pictures/screenshot.png
```

### With delay
```bash
gnome-screenshot -d 3 -f ~/Pictures/screenshot.png
```

### Select area
```bash
gnome-screenshot -a -f ~/Pictures/screenshot.png
```

### Current window
```bash
gnome-screenshot -w -f ~/Pictures/screenshot.png
```

### To clipboard
```bash
gnome-screenshot -c
```

## Capture Screenshots with maim

### Full screen
```bash
maim ~/Pictures/screenshot.png
```

### Select region
```bash
maim -s ~/Pictures/screenshot.png
```

### Select window
```bash
maim -i $(xdotool getactivewindow) ~/Pictures/window.png
```

### Specific region (x,y,width,height)
```bash
maim -g 100x100+500+300 ~/Pictures/region.png
```

### High quality
```bash
maim -m 10 ~/Pictures/screenshot.png
```

## Screen Recording

### Record screen with ffmpeg
```bash
ffmpeg -video_size 1920x1080 -framerate 30 -f x11grab -i :0.0 -c:v libx264 -preset ultrafast output.mp4
```

### Stop recording
Press `q` in the terminal or `Ctrl+C`.

### Record with audio
```bash
ffmpeg -video_size 1920x1080 -framerate 30 -f x11grab -i :0.0 -f pulse -i default -c:v libx264 -preset ultrafast -c:a aac output.mp4
```

## Notes
- Linux-only (alternative to macOS Peekaboo).
- `scrot` is lightweight and widely available.
- `maim` offers more advanced features.
- `gnome-screenshot` integrates well with GNOME desktop.
- For Wayland, use `grim` instead of `scrot`.
