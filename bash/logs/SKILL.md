---
name: logs
description: 'Fan out gateway logs across selected instances, redacted, with per-instance headers Arguments: [selector] [--tail <n>] [--since <dur>] [--grep <re>] [--errors-only].'
---

# Fleet logs

Read the runtime log of every selected instance in one pass. Read-only. Parse
`[selector] [--tail <n>] [--since <dur>] [--grep <re>] [--errors-only]` from "$ARGUMENTS";
defaults `--tail 200`, no `--since`, empty selector means every managed instance.

## 1. Resolve the targets
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" resolve "<selector>" --json \
  | python3 -c 'import json,sys
for i in json.load(sys.stdin)["instances"]:
    c, s = i.get("container") or {}, i.get("signals") or {}
    print(i["name"], i["state"], c.get("id") or "-", i["project"], s.get("log_age_hours"))'
```
`all` is allowed here — this command only reads. An `alien` row still gets its log read; it just gets no
interpretation, because nothing here knows what it is.

## 2. Read each instance, redact, then filter
```bash
docker logs --timestamps --tail <n> [--since <dur>] <container-id> 2>&1 \
  | python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lib/redact.py" \
  | grep -Ei '<pattern>'
```
**The order is the point: redact before filtering, never after.** A grep in front of the scrubber sends
raw matched lines to a sink that was never cleaned. `[scrubbed: N matches]` on stderr is the mechanism
working, not a warning; the redactor deliberately over-matches high-entropy strings.

- `--errors-only` → `grep -Ei 'error|fatal|panic|exception|unauthor|refused|timeout|ECONN'`.
- `--grep <re>` → that expression, `-E`. Both given: `--grep` narrows inside `--errors-only`.
- No container (`down`, absent) → `docker compose -p <project> logs --no-color --tail <n>` through the
  same redactor. Still nothing → say the instance has no runtime log rather than inventing one.

## 3. Print
One block per instance, in the resolve order, each opened by a header naming the instance, its state and
its log age so an empty block reads as evidence instead of an error:

```
==> <name>  state=<state>  log-age=<h>h  <==
```

## Hard rules
- Never `cat`, `tail` or `grep` a log file on the host, and never read a credential, `.env`,
  `auth-secrets` or auth-profile file to explain a log line. The container's own log stream through the
  redactor is the whole surface.
- Never paste a raw log line into a summary. Quote the redacted line as printed.
- Keep it bounded: past `--tail 2000` or a fleet-wide `--since 7d`, narrow the selector or the window
  instead — a wall of scrollback buries the one line that mattered.
- A crash loop is read here first and restarted never: a restart destroys the lines holding the cause and
  buys a longer backoff.

## Next
A log line that names a symptom but not an id → skill `fleet-diagnostics`. A green instance whose log has
not moved → `/openclaw-ops:status --deep` for the HEALTH/LIVENESS split. One CLI call against the same
instance → `/openclaw-ops:exec`.