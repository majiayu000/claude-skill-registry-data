---
name: listen
description: >-
  Speech-to-text via node .rulesync/scripts/listen.mjs (ffmpeg mic + local whisper.cpp,
  OpenAI fallback). Input only.
---
# listen

When the user wants to dictate, transcribe a recording, or toggle a mic, run `node .rulesync/scripts/listen.mjs`. Spec: `.rulesync/reference/listen.md`. Input only (audio → text). Do not speak. Do not use `/speak`.

`whoami` · `devices` · `rec [--seconds N]` · `start` · `stop` · `toggle` · `status` · `file --path P` · `latest`. `--clip` copies the transcript. `--cwd DIR` when the process is not already in the repo (hotkeys). `rec` prints the transcript and `transcript=.tmp/grunt/listen/latest.txt`.

STT: local `whisper-cli` first (mac: `brew install whisper-cpp`); first listen downloads the ggml model to `~/.grunt/whisper/`. Else `OPENAI_API_KEY`. Mic verbs need ffmpeg. Do not tell them to pip-install openai-whisper or curl the model by hand.

If the CLI exits non-zero, print its message. Lines with `setup:` are for the user — show that command. Tell them to run `node .rulesync/scripts/setup.mjs listen` (or `grunt setup`) in their terminal. Do not dump JSON. Do not invent a key. Spec: `.rulesync/reference/listen.md` `.rulesync/reference/setup.md`.
