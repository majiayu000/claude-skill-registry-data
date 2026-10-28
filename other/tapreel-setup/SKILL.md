---
name: tapreel-setup
description: Check and install what Tapreel needs (VoiceStudio, FilmCraft, ffmpeg, Playwright) before making a video. Use at the start of any Tapreel job, or when a Tapreel step fails because a tool is missing.
---

# Tapreel setup

Run `node <plugin>/bin/tapreel.mjs doctor`. It reports what is missing and installs nothing.
For each missing tool, **ask the user before installing**, in this form:
"Tapreel needs <tool> to <why>. It isn't installed. Install it now? (yes / no)".
If they say no to a required tool, stop and say: "Tapreel can't run without it."

| Need | Why | Check | Install (only after the user says yes) |
|---|---|---|---|
| VoiceStudio | the local voice that narrates | `GET http://localhost:3900/profiles` answers | https://github.com/debpalash/VoiceStudio, install and start the app |
| ffmpeg | encoding and loudness | `ffmpeg -version` | `winget install Gyan.FFmpeg` / `brew install ffmpeg` |
| Playwright + Chromium | operating and recording the app | `doctor` says ok | `npm install` in the plugin folder, then `npx playwright install chromium` |
| FilmCraft (optional editor) | extra editing after the film is built | `filmcraft-cli --version` | https://github.com/storytold/filmcraft |

Also needed: a narrator voice. Set `voice.profileId` in the config to one of the profiles `doctor` lists, or design or clone one in VoiceStudio (clone only a voice whose owner has agreed).

Never install silently. Never print or store secrets.
