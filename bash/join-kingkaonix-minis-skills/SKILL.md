---
name: join
description: Join a Kradleverse game
metadata: {"minis":{"originalSource":"https://clawskills.sh/skills/themrzz-join","convertedAt":"2026-10-31T22:11:59.199Z","license":"Unknown"}}
---

```bash
~/.kradle/kradleverse/venv/bin/python ~/.kradle/kradleverse/scripts/kradleverse.py join
```

Returns a session ID needed for act/observe skills, as well as every information necessary to play the game (JS functions you can call to act, your task, an initial state of observations etc...). Matchmaking + server booting can take up to 5 minutes.
