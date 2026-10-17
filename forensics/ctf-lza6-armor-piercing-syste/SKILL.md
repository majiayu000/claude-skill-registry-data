---
name: ctf
description: >-
  CTF methodology with optional Deep Eye on lab targets you own. Use for CTF,
  HTB, picoCTF, web/pwn/rev/crypto/forensics, /ctf. Educational only.
---

# Deep Eye — CTF Skill

Only scan labs you own or are allowed to attack.

## Loop

Read → classify → inventory → hypotheses → exploit → writeup.

## Web labs + Deep Eye

```bash
python deep_eye.py -u http://LAB:PORT -v --formats json
```

Helpful: `ssti`/`ssti_engines`, `sql_injection`, `xss`, `jwt_deep`, `lfi`, `ssrf`, `php_webshell`, `graphql_deep`.
Multi-surface inject: `core/injection_surfaces.py`.

## Categories

Web / crypto / pwn / rev / forensics / OSINT — standard CTF method; flag formats vary.

## Writeup

```markdown
# Name
- Idea / steps / flag / lesson
```

## Rules

No real third-party attacks for practice; honor spoiler policies.
