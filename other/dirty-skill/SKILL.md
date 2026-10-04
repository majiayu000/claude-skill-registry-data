---
name: dirty-skill
description: A deliberately leaky demo skill used to show what skill-sanitizer catches before you publish. Do not ship this.
---

# dirty-skill (DEMO — intentionally leaky)

This folder is a teaching fixture for `skill-sanitizer`. It contains planted,
clearly-fake-but-realistic leaks so you can watch the scanner BLOCK on a publish
attempt. **Nothing here is a real credential** — the values are dummies sized to
look real so the scanner treats them seriously.

## What is planted (one per leak class)

| Class | Where | Planted value (fake) |
|-------|-------|----------------------|
| SECRET | `sync.py:5` | a `ghp_` GitHub token (36 hex-ish chars) → hard **BLOCK** |
| PROPRIETARY | `sync.py:8` | a hardcoded home-dir path with a username → WARN |
| PII | `sync.py:11` | a personal `gmail.com` email → WARN |
| SERVICE CODE | `sync.py` | an internal Jira marker (`.atlassian.net`, `customfield_*`) → `plugin-split` advice |

## Run it

```bash
cd examples/dirty-skill
python ../../scanner.py .
```

Expected: a report with `BLOCK=2 WARN=4` and **exit code 1**. The full expected
report is in [`../EXPECTED_OUTPUT.md`](../EXPECTED_OUTPUT.md). Fixing the four
planted leaks (env-var the token, swap the path for `~`, use an `example.com`
email, move the Jira code to a plugin) takes the same folder to **exit 0**.
