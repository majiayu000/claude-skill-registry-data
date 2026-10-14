---
name: linux-apps
description: "Manage and control Linux applications. List running apps, start/stop apps, capture window screenshots, focus/minimize/maximize windows, and get app info. Use when a user asks FRIDAY to manage apps, see what's running, or take a screenshot of a specific app."
homepage: https://docs.friday.ai/tools/linux-apps
metadata: {"friday":{"emoji":"🖥️","os":["linux"],"requires":{"bins":["wmctrl"]},"install":[{"id":"apt-wmctrl","kind":"apt","package":"wmctrl","bins":["wmctrl"],"label":"Install wmctrl via apt"}]}}
---

# Linux App Manager

Manage and control Linux desktop applications. List running apps, control windows, and capture screenshots of specific applications.

## Setup
Install required tools:
```bash
sudo apt-get install -y wmctrl xdotool scrot xwininfo imagemagick
```

## List Running Applications

### List all windows with details
```bash
wmctrl -l -p -G
```
Output: `<window_id> <desktop> <pid> <x> <y> <width> <height> <client_machine> <title>`

### List windows with class names
```bash
wmctrl -l -x
```

### List only window titles (clean)
```bash
wmctrl -l | awk '{$1=$2=$3=""; print substr($0,4)}'
```

### Get window count
```bash
wmctrl -l | wc -l
```

### List running processes (GUI apps)
```bash
ps aux | grep -E 'code|firefox|chrome|slack|discord|spotify|vlc|nautilus|terminal' | grep -v grep
```

## Start Applications

### Launch common apps
```bash
# Browser
firefox &
google-chrome &
brave-browser &

# Code editor
code &
code /path/to/project &

# File manager
nautilus ~ &

# Terminal
gnome-terminal &
xterm &

# Media
vlc /path/to/video &
spotify &
```

### Launch and wait for window to appear
```bash
firefox & sleep 2 && wmctrl -a Firefox
```

### Open file with default app
```bash
xdg-open ~/Documents/file.pdf
xdg-open https://example.com
xdg-open ~/Pictures/image.png
```

## Stop/Close Applications

### Close window gracefully (by title)
```bash
wmctrl -c "Firefox"
wmctrl -c "Visual Studio Code"
```

### Close active window
```bash
xdotool getactivewindow windowclose
```

### Force kill app (by name)
```bash
pkill firefox
pkill -9 code  # Force kill
```

### Kill by window ID
```bash
xdotool windowclose <window_id>
```

## Window Control

### Focus/activate a window
```bash
wmctrl -a "Firefox"              # By title (partial match)
wmctrl -i -a 0x04000007          # By window ID
xdotool search --name "Firefox" windowactivate
```

### Minimize window
```bash
xdotool getactivewindow windowminimize
xdotool search --name "Firefox" windowminimize
```

### Maximize window
```bash
wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz
wmctrl -r "Firefox" -b add,maximized_vert,maximized_horz
```

### Unmaximize (restore)
```bash
wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz
```

### Toggle fullscreen
```bash
wmctrl -r :ACTIVE: -b toggle,fullscreen
```

### Move window to position
```bash
wmctrl -r :ACTIVE: -e 0,100,100,-1,-1   # Move to x=100, y=100
wmctrl -r "Firefox" -e 0,0,0,1920,1080  # Position and resize
```

### Resize window
```bash
wmctrl -r :ACTIVE: -e 0,-1,-1,800,600   # Resize to 800x600
xdotool getactivewindow windowsize 800 600
```

### Move to desktop/workspace
```bash
wmctrl -r :ACTIVE: -t 1   # Move to desktop 1 (0-indexed)
```

### Bring window to front (raise)
```bash
wmctrl -a "Firefox"
xdotool search --name "Firefox" windowraise
```

## Capture App Screenshots

### Screenshot active window
```bash
scrot -u ~/Pictures/window-$(date +%Y%m%d-%H%M%S).png
```

### Screenshot specific window by name
First get window ID, then capture:
```bash
# Get window ID
WIN_ID=$(xdotool search --name "Firefox" | head -1)
# Capture that window
import -window $WIN_ID ~/Pictures/firefox-screenshot.png
```

### Screenshot window by clicking (interactive)
```bash
scrot -s ~/Pictures/selected-$(date +%Y%m%d-%H%M%S).png
```

### Screenshot with ImageMagick (by window ID)
```bash
# Get window geometry first
WIN_ID=$(xdotool search --name "Firefox" | head -1)
import -window $WIN_ID ~/Pictures/app-screenshot.png
```

### Screenshot window including decorations
```bash
scrot -ub ~/Pictures/window-with-border.png
```

### One-liner: Screenshot specific app
```bash
# Firefox
xdotool search --name "Firefox" | head -1 | xargs -I{} import -window {} ~/Pictures/firefox.png

# VS Code
xdotool search --name "Visual Studio Code" | head -1 | xargs -I{} import -window {} ~/Pictures/vscode.png
```

### Screenshot and display path
```bash
FILE=~/Pictures/app-$(date +%Y%m%d-%H%M%S).png && scrot -u "$FILE" && echo "Saved: $FILE"
```

## Get App/Window Information

### Get active window info
```bash
xdotool getactivewindow getwindowname
xdotool getactivewindow getwindowpid
xdotool getactivewindow getwindowgeometry
```

### Get window geometry (size and position)
```bash
xwininfo -id $(xdotool getactivewindow)
```

### Find window by app name
```bash
xdotool search --name "Firefox"
xdotool search --class "code"
```

### Get PID of window
```bash
xdotool search --name "Firefox" | head -1 | xargs -I{} xdotool getwindowpid {}
```

### Check if app is running
```bash
pgrep -x firefox && echo "Firefox is running" || echo "Firefox is not running"
```

### Get app resource usage
```bash
# CPU and memory for specific app
ps aux | grep firefox | grep -v grep

# More details
top -bn1 | grep firefox
```

## Common Workflows

### Switch to app (or launch if not running)
```bash
wmctrl -a "Firefox" || firefox &
```

### Tile two windows side by side
```bash
# Left half
wmctrl -r "Firefox" -e 0,0,0,960,1080
# Right half
wmctrl -r "Code" -e 0,960,0,960,1080
```

### Close all windows of an app
```bash
xdotool search --name "Firefox" | xargs -I{} xdotool windowclose {}
```

### Screenshot all open windows
```bash
mkdir -p ~/Pictures/windows-$(date +%Y%m%d)
for wid in $(xdotool search --onlyvisible --name ""); do
  name=$(xdotool getwindowname $wid | tr ' /' '_')
  import -window $wid ~/Pictures/windows-$(date +%Y%m%d)/${name}.png 2>/dev/null
done
```

## Desktop Info

### List desktops/workspaces
```bash
wmctrl -d
```

### Switch desktop
```bash
wmctrl -s 1  # Switch to desktop 1
```

### Get screen resolution
```bash
xdpyinfo | grep dimensions
xrandr | grep '\*'
```

### Get display info
```bash
xrandr --query
```
