---
name: linux-media-control
description: Control media playback on Linux using playerctl. Play, pause, skip, control volume for Spotify, VLC, and other media players. Use when a user asks FRIDAY to play music, pause, skip track, or control media on Linux.
homepage: https://github.com/altdesktop/playerctl
metadata: {"friday":{"emoji":"🎵","os":["linux"],"requires":{"bins":["playerctl"]},"install":[{"id":"apt-playerctl","kind":"apt","package":"playerctl","bins":["playerctl"],"label":"Install playerctl via apt"}]}}
---

# Linux Media Control CLI

Use `playerctl` to control media players (Spotify, VLC, Firefox, Chrome, etc.) from the terminal. This is the standard way to control media on Linux.

## Setup
Install playerctl:
```bash
sudo apt-get install -y playerctl
```

## Basic Playback Control

### Play
```bash
playerctl play
```

### Pause
```bash
playerctl pause
```

### Toggle play/pause
```bash
playerctl play-pause
```

### Stop
```bash
playerctl stop
```

### Next track
```bash
playerctl next
```

### Previous track
```bash
playerctl previous
```

## Volume Control

### Get current volume
```bash
playerctl volume
```

### Set volume (0.0 to 1.0)
```bash
playerctl volume 0.5
```

### Increase volume
```bash
playerctl volume 0.1+
```

### Decrease volume
```bash
playerctl volume 0.1-
```

### Mute (set to 0)
```bash
playerctl volume 0
```

## Track Information

### Current track metadata
```bash
playerctl metadata
```

### Track title
```bash
playerctl metadata title
```

### Artist
```bash
playerctl metadata artist
```

### Album
```bash
playerctl metadata album
```

### Current position
```bash
playerctl position
```

### Track length
```bash
playerctl metadata mpris:length
```

### Album art URL
```bash
playerctl metadata mpris:artUrl
```

### Formatted output
```bash
playerctl metadata --format "{{ artist }} - {{ title }}"
```

## Seeking

### Go to position (seconds)
```bash
playerctl position 30
```

### Skip forward 10 seconds
```bash
playerctl position 10+
```

### Skip backward 10 seconds
```bash
playerctl position 10-
```

## Player Selection

### List available players
```bash
playerctl --list-all
```

### Control specific player
```bash
playerctl --player=spotify play
playerctl --player=vlc pause
playerctl --player=firefox next
```

### Control all players
```bash
playerctl --all-players pause
```

### Ignore specific player
```bash
playerctl --ignore-player=chromium play-pause
```

## Player Status

### Get playback status
```bash
playerctl status
```
Returns: `Playing`, `Paused`, or `Stopped`

### Check if playing
```bash
if [ "$(playerctl status)" = "Playing" ]; then
  echo "Music is playing"
fi
```

## Shuffle & Loop

### Get shuffle status
```bash
playerctl shuffle
```

### Enable/disable shuffle
```bash
playerctl shuffle on
playerctl shuffle off
playerctl shuffle toggle
```

### Get loop status
```bash
playerctl loop
```

### Set loop mode
```bash
playerctl loop None
playerctl loop Track
playerctl loop Playlist
```

## Advanced

### Open URI in player
```bash
playerctl open "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
playerctl open "https://example.com/song.mp3"
```

### Follow metadata changes (watch mode)
```bash
playerctl metadata --follow --format "Now playing: {{ artist }} - {{ title }}"
```

### Wait for player events
```bash
playerctl --follow status
```

## Spotify Specific

### List Spotify tracks
```bash
playerctl --player=spotify metadata
```

### Get Spotify track ID
```bash
playerctl --player=spotify metadata mpris:trackid
```

### Play specific Spotify URI
```bash
playerctl --player=spotify open spotify:track:TRACK_ID
```

## Scripts Examples

### Now Playing Notification
```bash
notify-send "Now Playing" "$(playerctl metadata --format '{{ artist }} - {{ title }}')"
```

### Auto-pause on lock
```bash
# Add to screen lock script
playerctl pause
```

### Toggle play and show status
```bash
playerctl play-pause
if [ "$(playerctl status)" = "Playing" ]; then
  notify-send "Playing" "$(playerctl metadata title)"
else
  notify-send "Paused"
fi
```

## System Volume (alternative)

### Using pactl (PulseAudio)
```bash
# Get volume
pactl get-sink-volume @DEFAULT_SINK@

# Set volume
pactl set-sink-volume @DEFAULT_SINK@ 50%

# Increase volume
pactl set-sink-volume @DEFAULT_SINK@ +10%

# Decrease volume
pactl set-sink-volume @DEFAULT_SINK@ -10%

# Mute toggle
pactl set-sink-mute @DEFAULT_SINK@ toggle
```

### Using amixer (ALSA)
```bash
# Increase volume
amixer set Master 10%+

# Decrease volume
amixer set Master 10%-

# Mute toggle
amixer set Master toggle
```

## Notes
- Linux-only.
- Works with MPRIS-compatible players (Spotify, VLC, Firefox, Chrome, etc.).
- Spotify must be running for Spotify commands to work.
- Use `playerctl --list-all` to see available players.
- Some features may vary by player.
