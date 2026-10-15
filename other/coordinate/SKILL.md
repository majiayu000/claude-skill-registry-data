---
name: coordinate
description: Run several Keelokit sessions at once and keep them honest — one session per story with the shared agent brief, status in ten lines, follow-up rounds, and verifying landed work by its hash on origin/main. Use when the user says "coordinate", "run these stories in parallel sessions", "status of the sessions", "¿cómo van las sesiones?", "coordiná las sesiones", "estado de las sesiones", or when several sessions or worktrees are running.
---

# Coordinate — origin/main is the only truth

The brief every session follows is `.keelokit/harness/agent-brief.md` (SESS-1). Read it once.

## Start sessions

- One session per story, from the same wave (the doctor guarantees their `touches` don't overlap).
  Stories that add migrations go one at a time (MIG-1).
- The prompt is short: `Read .keelokit/harness/agent-brief.md, then /keelokit:build-story <ID>.` Pass paths, not
  contents; don't repeat the brief's rules.
- Respect the machine: at most two sessions running tests at once (`pnpm verify` takes a per-machine
  lock, so more only wait).

## Every round (about every 15 minutes while sessions run)

1. `python3 .keelokit/bin/status.py`: worktrees, branches with commits not on `origin/main`, the
   verify lock, the CI of main (a cancelled run is not green) and the backlog, in ten lines.
2. For each session that says it finished: `git fetch origin main && git log origin/main --oneline`
   and find its commit (`Story: <ID>` trailer). **A session that ends well does not message you; don't wait for
   a message, check the hash.** "Done" without a commit on main is not done: send it back to land
   (rebase, `pnpm verify`, push) or land it yourself.
3. CI of main red, or two runs in a row without a green: stop starting stories; `python3
   .keelokit/bin/ci.py jobs` says which job and step; fix that first.
4. Wait with one `until` loop on one condition, never with repeated polling.

## Report to the user

Two lines per session at most: story, hash on main (or "not landed" and why), then what needs the
user. The whole report fits in ten lines.
