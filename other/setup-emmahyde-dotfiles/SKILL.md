---
name: wispr:setup
description: Interactive setup wizard for the Wispr Voice plugin. Configures ~/.claude/wispr-config.yml, checks Wispr Flow is installed, and collects trigger word, TTS voice, and terminal app filter.
---

Walk the user through setup interactively. Use `AskUserQuestion` for each prompt. Read any existing `~/.claude/wispr-config.yml` first and pre-fill answers with current values.

## Step 1 — Check Wispr Flow is installed

```bash
[[ -f "$HOME/Library/Application Support/Wispr Flow/flow.sqlite" ]] && echo "found" || echo "missing"
```

If missing: tell the user Wispr Flow doesn't appear to be installed or hasn't been opened yet, and ask them to open it before continuing. Wait for confirmation.

## Step 2 — Trigger word

Explain: Without a trigger word, **every dictation you make — in any app, at any time — will be forwarded to Claude**. A trigger word limits capture to dictations that start with that word, regardless of which app is in focus.

Ask: `What trigger word should gate dictations? (default: claude — leave blank to capture all dictations)`

## Step 3 — Terminal app filter

Explain: The app filter limits forwarding to dictations made while a specific app is active (frontmost window). Note: **the terminal does not need to be the active window** — Wispr captures dictations system-wide, so this filter works by matching the app that was focused when you spoke, not the app Claude is running in.

Ask: `Do you want to filter to dictations from your terminal app only? (y/n)`

If yes, ask: `What is your terminal app called? (e.g. iTerm2, Terminal, Warp)` — then resolve its bundle ID:

```bash
osascript -e 'id of app "<name>"'
```

Show the resolved bundle ID and confirm with the user.

## Step 4 — TTS voice

List Premium voices available on the system:

```bash
say -v '?' | grep -i premium | awk '{print $1, $2}' | sort
```

If any Premium voices are found, show the list and explain:
> These are Apple's high-quality neural voices — no API key or external service needed.

Ask: `Which voice would you like to use? (enter a name from the list, or press Enter for Samantha)`

If no Premium voices are found:

1. Tell the user no Premium voices are installed and open the System Settings pane automatically:

```bash
open "x-apple.systempreferences:com.apple.preference.universalaccess?Spoken"
```

2. Instruct them: "System Settings is opening to Spoken Content. Click **System Voice → Manage Voices**, then download any voice marked **Premium**. Come back here when done."

3. Ask: `Press Enter once you've downloaded a Premium voice (or type "skip" to use a standard voice)`

4. If they pressed Enter (not skip), re-run the Premium voice check:

```bash
say -v '?' | grep -i premium | awk '{print $1, $2}' | sort
```

If voices now appear, show the list and ask which to use. If still none, proceed with standard voices.

5. If they typed "skip" or still no Premium voices: run `say -v '?' | grep -vi premium | awk '{print $1}' | sort` and ask which standard voice to use (default: Samantha).

## Step 5 — Write config

Write `~/.claude/wispr-config.yml` with all collected values:

```yaml
# Wispr Voice plugin configuration
trigger_word: <value or empty>

# Terminal app filter — only forward dictations from this app (leave blank for all apps).
# Note: the terminal does not need to be the active window for dictation to work.
# Find bundle ID: osascript -e 'id of app "YourApp"'
wispr_app: <bundle-id or empty>

# macOS say voice for TTS responses
wispr_voice: <voice name>
```

Fill in or comment out fields based on what the user provided.

## Step 6 — Done

Tell the user setup is complete and they can run `/wispr:on` to start the monitor. Show a one-line summary of what was configured (trigger word, voice, app filter if set).
