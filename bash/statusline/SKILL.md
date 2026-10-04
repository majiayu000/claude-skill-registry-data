---
description: Add a live pi dispatch indicator to the Claude Code status line, composed with whatever status line the user already has
disable-model-invocation: true
---

The user wants the pi indicator in their status line: $ARGUMENTS

`statusLine` is a **single global field** in `~/.claude/settings.json`. There is exactly one,
and a plugin cannot ship its own — the plugin `settings.json` supports only `agent` and
`subagentStatusLine`. So there is no way to add this without writing to the user's settings,
and every step below exists because of that: whatever is already there is theirs, it is
probably the only status line they have, and replacing it is not a thing to do quietly.

Work through this with them. Do not run it end to end and report afterwards.

## 1. Find out what is already there

```bash
python3 -c "
import json, os
p = os.path.expanduser('~/.claude/settings.json')
d = json.load(open(p)) if os.path.exists(p) else {}
print(json.dumps(d.get('statusLine', None), indent=2))
print('refreshInterval:', (d.get('statusLine') or {}).get('refreshInterval', '(unset)'))
"
```

**If the command contains `pi-delegate/statusline-wrapper.sh`, it is already ours.** Stop and
go to step 6 (update in place). Wrapping a wrapper is the obvious way to end up running the
user's real status line twice, and then four times.

## 2. Probe it — do not reason about it

Whatever is there, run it and look. It gets a JSON payload on stdin, so give it one:

```bash
printf '%s' '{"session_id":"probe","cwd":"'"$PWD"'","model":{"id":"claude-opus-5","display_name":"Opus 5"},"workspace":{"current_dir":"'"$PWD"'","project_dir":"'"$PWD"'"},"version":"2.0.0","context_window":{"used_percentage":25}}' \
  | <their command> > /tmp/pi-probe.out 2>/tmp/pi-probe.err
echo "exit=$?  lines=$(wc -l < /tmp/pi-probe.out)"
cat /tmp/pi-probe.out
```

This is the whole reason the composition is safe for people whose setup you have never seen.
You are not guessing at ccstatusline, starship, powerline or a personal shell script — you are
looking at the bytes it produced. Note the line count; that is what the "after" preview needs.

Then show them their pi segment, on its own:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/statusline.sh"
```

If nothing is running it prints nothing, which is correct and worth saying out loud — the row
only exists while a dispatch is in flight. To show them what it will look like, fake one:

```bash
mkdir -p ~/.claude/pi-delegate/status
{ echo "pid=$$ running=2 oldest=$(( $(date +%s) - 192 )) updated=$(date +%s) models=Qwen3.8-27B"
  echo "$CLAUDE_CODE_MESSAGING_SOCKET"; } > ~/.claude/pi-delegate/status/preview.status
"${CLAUDE_PLUGIN_ROOT}/scripts/statusline.sh"
rm ~/.claude/pi-delegate/status/preview.status
```

The second line is the owner: the session that wrote the file. The reader shows only files
whose owner matches its own, so a preview written without it renders nothing — and so does
another Claude Code window's real dispatch, which is the point.

Show them **before and after** — their real output, then their real output with the pi row
under it — and ask before writing anything.

## 3. Say what it costs, before they answer

Two things, and neither is obvious from the preview:

- **`refreshInterval` is required, not decorative.** Without it the status line only reruns on
  conversation events, and those go quiet exactly when an async dispatch is running and the
  session is idle — which is the entire case this feature exists for. The recommended value is
  **`1`**, the minimum Claude Code allows.
- **Why `1` and not something cheaper:** the default row shows an elapsed seconds counter, and
  a counter refreshed every 2 seconds skips numbers — 8s, 10s, 12s. That reads as broken rather
  than as slow, and it is the first thing anyone notices. Anything above `1` needs the counter
  taken out of `fmt_elapsed` (show only minutes, or drop the duration) to look deliberate.
- **`refreshInterval` reruns the whole thing, including their existing status line.** If theirs
  shells out to `git` (most do), that is now running every second for as long as Claude Code is
  open. Use the timing you measured in step 2: a status line taking ~100ms is roughly 10% of one
  core at `1`, 5% at `2`. If their probe was slow, say the number and offer `2` or `3` — paired
  with editing `fmt_elapsed` so the seconds counter is not left skipping.
- **How many rows it can take.** There is one row per running dispatch, capped at `MAX_ROWS`
  (4) with a `… +N more` line beyond that. Added to whatever they already have, that is their
  existing height plus up to five. Worth saying out loud to anyone whose status line is already
  two or three lines tall; `MAX_ROWS` is theirs to lower.

If they would rather not have the timer, the indicator still works — it just only updates when
something else already caused a redraw. Say that plainly rather than talking them into the timer.

## 4. Install their own copy of the segment

Copy the script to a stable path instead of pointing settings at the plugin:

```bash
mkdir -p ~/.claude/pi-delegate
cp "${CLAUDE_PLUGIN_ROOT}/scripts/statusline.sh" ~/.claude/pi-delegate/statusline.sh
chmod +x ~/.claude/pi-delegate/statusline.sh
```

The plugin's own path carries its version (`.../pi-delegate/0.13.1/...`) and every release gets
a new directory, so a `settings.json` pointing into it breaks on the next `/plugin update` —
silently, because a status line that fails just doesn't render.

**This copy is also where the user's taste goes.** The script separates gathering from
rendering: everything above the `render` banner collects the facts — including deciding which
status files are this session's — and `render_row` alone decides what a row looks like. It is
called once per running dispatch with `started`, `count` and `model`, plus `$DOT` and `$now`;
`fmt_elapsed` formats the duration and `MAX_ROWS` caps how many rows print. If they want
different wording, no breathing dot, a different colour, their own glyphs, minutes instead of
seconds, fewer rows — that is all inside those three. Offer this; it is the point of the file
being shaped that way. Leave everything above the banner alone, ownership check included.

**One row per dispatch is the contract, not a detail.** Two dispatches started ten minutes
apart get a row each, with their own elapsed and their own colour threshold, because a single
aggregated row could only ever tell the truth about the older of them. If they edit
`render_row` into something multi-line, `MAX_ROWS` stops bounding the height and the status bar
can grow without limit — worth saying if they start redesigning it.

## 5. Compose, back up, and write

Back up first, with a timestamp, and tell them the path:

```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak.$(date +%Y%m%d-%H%M%S)
```

Write the wrapper. Substitute their real command into `PI_DELEGATE_ORIGINAL` (single-quoted,
with any embedded `'` escaped as `'\''`), or leave it empty if they had no status line:

```bash
cat > ~/.claude/pi-delegate/statusline-wrapper.sh <<'WRAPPER'
#!/usr/bin/env bash
# Generated by /pi-delegate:statusline. Runs the status line that was configured before
# pi-delegate touched it, then appends the pi row underneath when a dispatch is running.
#
# To restore the original: put PI_DELEGATE_ORIGINAL back as settings.json's
# statusLine.command, or just run /pi-delegate:statusline and ask to remove it.
PI_DELEGATE_ORIGINAL=''

# Deliberately NO `set -e`. The two halves must not be able to take each other down: a
# broken status line is present on every screen the user looks at, so a failure in one half
# has to degrade to "that half is missing", never to an empty bar.

# stdin can only be read once, and both halves want it.
input=$(cat)

if [ -n "$PI_DELEGATE_ORIGINAL" ]; then
  printf '%s' "$input" | eval "$PI_DELEGATE_ORIGINAL" || true
fi

# Prints nothing at all unless a pi dispatch is running, so this row costs no height when
# there is nothing to say.
[ -x "$HOME/.claude/pi-delegate/statusline.sh" ] && "$HOME/.claude/pi-delegate/statusline.sh" || true

exit 0
WRAPPER
chmod +x ~/.claude/pi-delegate/statusline-wrapper.sh
```

Then point settings at it, preserving every other key:

```bash
python3 - <<'PY'
import json, os
p = os.path.expanduser('~/.claude/settings.json')
d = json.load(open(p)) if os.path.exists(p) else {}
d['statusLine'] = {
    'type': 'command',
    'command': os.path.expanduser('~/.claude/pi-delegate/statusline-wrapper.sh'),
    'refreshInterval': 1,
}
json.dump(d, open(p, 'w'), indent=2)
open(p, 'a').write('\n')
print('statusLine ->', d['statusLine'])
PY
```

Verify by running the wrapper the same way Claude Code will, and show them the result:

```bash
printf '%s' '{"session_id":"probe","cwd":"'"$PWD"'","model":{"display_name":"Opus 5"},"workspace":{"current_dir":"'"$PWD"'","project_dir":"'"$PWD"'"}}' \
  | ~/.claude/pi-delegate/statusline-wrapper.sh
```

If that prints their original status line unchanged, the composition worked. The pi row appears
on the next real dispatch. Tell them it takes effect immediately — no reload needed.

## 6. Updating or removing it later

**Updating after a plugin upgrade:** re-run step 4's `cp`. Warn them first if they edited
`render` — the copy is theirs, and overwriting it silently would throw their work away. Diff it
against the plugin's version and let them decide.

**Removing it:** read `PI_DELEGATE_ORIGINAL` out of the wrapper, put it back as
`statusLine.command`, and drop `refreshInterval` if they did not have one before (check the
backup). If `PI_DELEGATE_ORIGINAL` is empty they had no status line, so remove the `statusLine`
key entirely rather than leaving one that prints only pi rows.

## What this deliberately does not do

It does not put pi into the subagent panel below the prompt. `subagentStatusLine` can only
override the rows Claude Code already renders for its own subagents — override one by `id`,
or hide it with an empty string. There is no way to add a row, and a pi dispatch is not a
Claude Code subagent. The main status line is the only surface available, so the pi row
imitates that style rather than living there.
