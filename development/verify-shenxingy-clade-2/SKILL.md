---
name: verify
description: Verify project behavior anchors — compilation, tests, and interaction checks after autonomous runs. NOT the Claude Code built-in /verify (which runs the app to observe a single change working) — this one walks the CLAUDE.md "Features (Behavior Anchors)" list.
when_to_use: "verify project, run checks, syntax check, build check, verify anchors"
user_invocable: false
---

# Verify Skill

Post-iteration verification used by `start.sh` to check that behavior anchors still pass after autonomous work. Not user-invocable — called internally by the autonomous loop.
