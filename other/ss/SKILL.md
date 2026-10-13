---
name: ss
description: "Load screenshots, shared files, or directories from the Dropbox screenshots directory — the shorthand for '/db screenshots/'. Use when the user invokes /ss, including inline forms like '/ss webdaw/ use its docs'. NEVER manually list/read files from the screenshots dir — this skill handles Dropbox sync delays, freshness checks and retry logic that manual reads miss. Supports: /ss (latest 1), /ss 2 or /ss latest3 (latest N), /ss filename.png (exact or substring), /ss dirname/, /ss full-path, /ss a.png b.png (multiple), and non-image files (/ss report.html)."
disable-model-invocation: false
argument-hint: "[N | latestN | filename | dirname/ | file1 file2 ...]"
allowed-tools: Read, Bash(ls *), Bash(find *), Bash(stat *), Bash(for *), Bash(while *), Bash(head *), Bash(seq *), Bash(sleep *), Bash(printf *), Bash(sort *), Bash(cut *)
---

# Screenshot loader

`/ss <arg>` is `/db screenshots/<arg>`, plus the latest-N selection below — the user shares a screenshot and invokes `/ss` within seconds, so "the newest file" needs its own handling.

**Invocation epoch:** !`date +%s`

Keep this as `CUTOFF`. In latest-N mode, only files with mtime `<= CUTOFF` are eligible, so a screenshot taken *after* the user typed `/ss` can never displace the one they meant.

## Base directory

`$DROPBOX_SCREENSHOTS_DIR` (= `$DROPBOX_ROOT/screenshots`). If unset or missing, stop and say so — do not guess. On Claude Code web this is expected: report that the screenshot is unreachable rather than substituting another file.

## Resolve the argument

Read `$HOME/.claude/skills/db/references/resolve.md` and apply it with **BASE = `$DROPBOX_SCREENSHOTS_DIR`** for every mode except latest-N: directories, exact and substring filenames, multiple files, non-image types, sync-delay retries, placeholder materialization.

Latest-N is the one mode that engine does not cover — it is below.

## Latest N images

Triggered by an empty argument (N = 1), a bare number (`/ss 2`), or `latestN` (`/ss latest3`). These are never multi-file arguments.

1. **Sleep 3 seconds first.** The screenshot is usually still syncing; this alone prevents the most common failure, returning yesterday's file.
2. List top-level images (`png jpg jpeg gif webp tiff`), keep mtime `<= CUTOFF`, newest first, take N.
3. **Freshness check:** the newest result must have mtime `>= CUTOFF - 120`. If everything is older, the new screenshot has not landed yet.
4. If stale, re-list every 5 seconds for up to 24 rounds.
5. On timeout, present what exists **with an explicit stale warning** — never silently pass off an old file as the requested one.

```bash
# mtime_of() is defined in resolve.md — redefine it in this shell first
CUTOFF=<invocation epoch>
FRESH=$((CUTOFF - 120))
sleep 3
for i in $(seq 1 24); do
  FILES=$(find "$DROPBOX_SCREENSHOTS_DIR" -maxdepth 1 -type f \
    \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
       -o -iname '*.gif' -o -iname '*.webp' -o -iname '*.tiff' \) 2>/dev/null |
    while IFS= read -r f; do
      m=$(mtime_of "$f"); [ -n "$m" ] && [ "$m" -le "$CUTOFF" ] && printf '%s\t%s\n' "$m" "$f"
    done | sort -rn | head -n "$N" | cut -f2-)
  NEWEST=$(printf '%s\n' "$FILES" | head -n 1)
  [ -n "$NEWEST" ] && [ "$(mtime_of "$NEWEST")" -ge "$FRESH" ] && break
  sleep 5
done
```

## Loaded screenshots are the context

The user just took these and invoked `/ss` — they are the request, not decoration. Never load them, judge them "not related", and carry on with the prior conversation. If they look obviously stale, apply the wait-and-recheck or ask step from `resolve.md` ("Loaded material is intentional context") — one or the other, never neither.

## Related skills

- `/db` — same engine from the Dropbox root, for anything outside `screenshots/`
