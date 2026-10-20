---
name: tmp-cleanup
description: Free memory by deleting stale artefacts from the temp dir (/tmp is often tmpfs, so it lives in RAM). Use when the user asks to free memory or clean up, when temp cleanup is requested, or when you notice memory pressure (low MemAvailable, swapping, OOM, large tmpfs usage).
---

# tmp-cleanup

On many Linux systems `/tmp` is tmpfs, so everything in it consumes RAM. The bundled
script `tmp-cleanup.sh` (next to this file) deletes stale top-level entries. It is a
script, rather than inline `rm -rf`, so the deletion rules (age, ownership, protected
names) are fixed and reviewable instead of improvised per call.

Works on Linux and macOS (bash 3.2+). Same skill format for Claude Code
(`~/.claude/skills/`) and Codex (`~/.codex/skills/` or `~/.agents/skills/`).

## Steps

1. Dry run first and show the count and size to the user:
   `<skill dir>/tmp-cleanup.sh`
2. Delete: `<skill dir>/tmp-cleanup.sh --apply`
   - Default age threshold is 3h; use `--hours N` if the user asks for another.
   - `--dir PATH` targets another directory (default `/tmp` on Linux, `$TMPDIR` on macOS).
   - On an explicit "free memory" / "cleanup" request, go straight to `--apply`.
   - On self-noticed memory pressure, dry-run, then ask before `--apply`.
3. Report only the before/after `df` lines. If memory is still tight, look at
   `du -sh /tmp/* 2>/dev/null | sort -h | tail` and tell the user about recent big
   offenders; don't delete entries newer than the threshold unasked.

## Safety

- Only top-level entries owned by the current user are touched.
- Protected by default: X/Qt locks and sockets, tmux, zellij, ssh, systemd-private,
  `*.lock`, `com.apple.*`, and the agents' own session dirs (`claude-*`, `cc-daemon-*`,
  `codex-*`).
- Protect more with `TMP_CLEANUP_KEEP="pattern1 pattern2"` or by editing the `keep` array.
- If the target isn't tmpfs (always the case on macOS) the script says deleting won't
  free RAM; tell the user instead of insisting.
- If your environment blocks recursive deletes (e.g. a hook), that's intentional: get
  the user's explicit OK before running `--apply` through the script.
