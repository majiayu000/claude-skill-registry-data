---
name: linux-ui-automation
description: Automate Linux desktop UI using xdotool and xclip. Simulate keyboard/mouse input, control windows, manage clipboard, and automate GUI applications. Use when a user asks FRIDAY to click, type, control windows, or automate UI on Linux.
homepage: https://github.com/jordansissel/xdotool
metadata: {"friday":{"emoji":"🖱️","os":["linux"],"requires":{"bins":["xdotool"]},"install":[{"id":"apt-xdotool","kind":"apt","package":"xdotool","bins":["xdotool"],"label":"Install xdotool via apt"}]}}
---

# Linux UI Automation CLI

Use `xdotool`, `wmctrl`, and `xclip` to automate Linux desktop UI. This is a Linux alternative to macOS Peekaboo automation features.

## Setup
Install required tools:
```bash
sudo apt-get install -y xdotool xclip wmctrl xwininfo
```

## Keyboard Input

### Type text
```bash
xdotool type "Hello World"
```

### Type with delay (ms between keys)
```bash
xdotool type --delay 50 "Hello World"
```

### Press key
```bash
xdotool key Return
xdotool key Escape
xdotool key Tab
xdotool key BackSpace
```

### Key combinations
```bash
xdotool key ctrl+c
xdotool key ctrl+v
xdotool key ctrl+shift+t
xdotool key alt+F4
xdotool key super
```

### Hold and release
```bash
xdotool keydown shift
xdotool type "hello"
xdotool keyup shift
```

## Mouse Input

### Move mouse to coordinates
```bash
xdotool mousemove 500 300
```

### Move relative
```bash
xdotool mousemove_relative 100 50
```

### Click
```bash
xdotool click 1  # Left click
xdotool click 2  # Middle click
xdotool click 3  # Right click
```

### Double click
```bash
xdotool click --repeat 2 --delay 50 1
```

### Click at position
```bash
xdotool mousemove 500 300 click 1
```

### Drag
```bash
xdotool mousemove 100 100
xdotool mousedown 1
xdotool mousemove 500 500
xdotool mouseup 1
```

### Scroll
```bash
xdotool click 4  # Scroll up
xdotool click 5  # Scroll down
```

### Scroll multiple times
```bash
xdotool click --repeat 5 --delay 50 5  # Scroll down 5 times
```

## Window Management

### Get active window ID
```bash
xdotool getactivewindow
```

### Focus window by name
```bash
xdotool search --name "Firefox" windowactivate
```

### Focus window by class
```bash
xdotool search --class "code" windowactivate
```

### List windows
```bash
wmctrl -l
```

### Activate window by title
```bash
wmctrl -a "Visual Studio Code"
```

### Minimize window
```bash
xdotool getactivewindow windowminimize
```

### Maximize window
```bash
wmctrl -r :ACTIVE: -b toggle,maximized_vert,maximized_horz
```

### Move window
```bash
xdotool getactivewindow windowmove 100 100
```

### Resize window
```bash
xdotool getactivewindow windowsize 800 600
```

### Close window
```bash
xdotool getactivewindow windowclose
```

### Bring window to front
```bash
wmctrl -a "Firefox"
```

## Clipboard

### Copy text to clipboard
```bash
echo "Hello World" | xclip -selection clipboard
```

### Paste from clipboard
```bash
xclip -selection clipboard -o
```

### Copy file contents to clipboard
```bash
cat file.txt | xclip -selection clipboard
```

### Copy image to clipboard
```bash
xclip -selection clipboard -t image/png -i image.png
```

### Copy from primary selection
```bash
xclip -selection primary -o
```

## Application Control

### Launch application
```bash
xdotool exec firefox
```

### Launch and wait for window
```bash
xdotool exec --sync firefox
```

### Get window PID
```bash
xdotool getactivewindow getwindowpid
```

### Kill window
```bash
xdotool getactivewindow getwindowpid | xargs kill
```

## Combined Workflows

### Open terminal and run command
```bash
xdotool key ctrl+alt+t
sleep 1
xdotool type "ls -la"
xdotool key Return
```

### Copy selected text
```bash
xdotool key ctrl+c
sleep 0.1
xclip -selection clipboard -o
```

### Paste text
```bash
echo "Text to paste" | xclip -selection clipboard
xdotool key ctrl+v
```

### Switch to window and type
```bash
xdotool search --name "Slack" windowactivate
sleep 0.5
xdotool type "Hello team!"
xdotool key Return
```

## Wait for Window

### Wait for window to appear
```bash
xdotool search --sync --name "Firefox"
```

### Wait and activate
```bash
xdotool search --sync --name "Dialog" windowactivate
```

## Get Window Info

### Window geometry
```bash
xdotool getactivewindow getwindowgeometry
```

### Window name
```bash
xdotool getactivewindow getwindowname
```

### All windows matching name
```bash
xdotool search --name "Code"
```

## Screen Info

### Get screen size
```bash
xdotool getdisplaygeometry
```

### Get mouse location
```bash
xdotool getmouselocation
```

## Notes
- Linux-only (alternative to macOS Peekaboo/keyboard maestro).
- Works with X11; for Wayland, use `ydotool` instead.
- Add delays between actions for reliability.
- Use `--sync` flag to wait for windows.
- Some applications may block synthetic input.
