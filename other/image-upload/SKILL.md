---
name: image-upload
description: Grab an image from the clipboard and analyze it. Use when the user says image upload, paste, screenshot, clipboard, or asks to look at something they copied.
---

Grab the user's clipboard image by detecting their OS and running the correct script:

**Windows:**
powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude\clipboard-grab.ps1"

**macOS:**
bash ~/.claude/clipboard-grab.sh

Run the appropriate command for the user's operating system. If you're unsure which OS, check with: uname -s (returns "Darwin" for macOS, or fails/returns something else on Windows).

If the output is a file path (not "NO_IMAGE"), read that image file. Briefly acknowledge what you see in one sentence, then wait for the user's instructions. Do NOT write a detailed description, table, or analysis. The user is sharing the image as context for their next message — treat it like they showed you their screen. Just confirm you see it and ask what they need, or if they included a message with the upload, respond to that.

If the output is "NO_IMAGE", tell the user no image was found in the clipboard and to copy an image first (Win+Shift+S on Windows, Cmd+Ctrl+Shift+4 on Mac, or copy from any app).

$ARGUMENTS
