---
name: wispr:off
description: Stop the Wispr Flow voice monitor.
---

Find and kill any active Wispr monitor processes:

```bash
for f in /tmp/wispr-session-current-*; do
  [[ ! -f "$f" ]] && continue
  PID="${f##*-}"
  kill "$PID" 2>/dev/null && echo "[wispr] stopped monitor (PID $PID)"
done
```

If no active monitor was found, tell the user. If one was stopped, confirm it's stopped.
