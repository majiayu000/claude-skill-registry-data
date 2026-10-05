---
name: analyzing-ios-app-security-with-objection
description: Local wrapper around the upstream Anthropic skill. Use for iOS runtime security assessment via Objection — SSL pinning bypass, keychain dump, jailbreak detection bypass, NSUserDefaults inspection, filesystem walk, cookie dump, IPA repackaging for non-jailbroken devices, OWASP Mobile Top 10 checklist. The upstream skill lives at skills/_upstream/anthropic-cybersecurity-skills/skills/analyzing-ios-app-security-with-objection/. In this repo, scripted Objection sequences live in objection_layer/scripts/ and are invoked via ObjectionRunner so their output lands in the engagement store.
---

# Objection (iOS) — wrapper

This is a wrapper around the upstream Anthropic skill. The full procedural reference is at:

- `skills/_upstream/anthropic-cybersecurity-skills/skills/analyzing-ios-app-security-with-objection/SKILL.md`
- `skills/_upstream/anthropic-cybersecurity-skills/skills/analyzing-ios-app-security-with-objection/references/workflows.md`
- `skills/_upstream/anthropic-cybersecurity-skills/skills/analyzing-ios-app-security-with-objection/scripts/agent.py`

Read those for the canonical workflow (OWASP Mobile Top 10 mapping, jailbroken vs non-jailbroken device matrix, etc.).

## How this repo extends the upstream skill

| Upstream concept | Local extension |
|---|---|
| Interactive `objection explore` | `objection_layer/runner.py` — scripted, deterministic |
| Ad-hoc commands | `objection_layer/scripts/*.objection` — versioned recipes |
| Text output | Per-script parsers turn output into `artifacts/*.json` |

## Scripts shipped

- `recon.objection` — env, frameworks, classes
- `ssl_pinning_check.objection` — observed pinning surface
- `keychain_dump.objection` — keychain inventory
- `jailbreak_detection.objection` — detection routine inspection
- `userdefaults_dump.objection`
- `cookies_dump.objection`

## When to use this skill vs the Frida skill

- **Objection** for breadth: fast recon, OWASP-aligned checks, structured commands.
- **Frida** for depth: a specific class, a specific method, a custom JS hook streaming events.

Use both — they share a target. Our planner runs Objection during Bootstrap for the recon pass, then keeps Frida hooks loaded throughout for sustained tracing.
