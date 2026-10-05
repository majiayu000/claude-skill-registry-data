---
name: reverse-engineering-ios-app-with-frida
description: Local wrapper around the upstream Anthropic skill. Use for iOS reverse engineering, Frida dynamic instrumentation, Objective-C / Swift method tracing, encryption key extraction, and runtime secret extraction. The upstream skill lives at skills/_upstream/anthropic-cybersecurity-skills/skills/reverse-engineering-ios-app-with-frida/ — read its SKILL.md and references/ for the procedural detail. When you would write your own Frida hook, prefer adding it to frida_layer/hooks/ and loading it via FridaRunner.load_hook so it streams events into the engagement store.
---

# Frida (iOS) — wrapper

This is a wrapper around the upstream Anthropic skill. The full procedural reference is at:

- `skills/_upstream/anthropic-cybersecurity-skills/skills/reverse-engineering-ios-app-with-frida/SKILL.md`
- `skills/_upstream/anthropic-cybersecurity-skills/skills/reverse-engineering-ios-app-with-frida/references/workflows.md`
- `skills/_upstream/anthropic-cybersecurity-skills/skills/reverse-engineering-ios-app-with-frida/scripts/agent.py`

Read those for the canonical workflow.

## How this repo extends the upstream skill

| Upstream concept | Local extension |
|---|---|
| One-shot `agent.py` Frida orchestrator | `frida_layer/runner.py` — async, message-pump into JSONL store |
| Ad-hoc hook examples | `frida_layer/hooks/*.js` — pinned, versioned, parameterizable |
| JSON dumps to `frida_ios/` | `runs/<run_id>/frida_events.jsonl` + SQLite indexes for query |
| Per-script outputs | Correlated with HTTP flows via `agent/correlate.py` |
| Manual reporting | Auto-rendered Markdown findings via `templates/finding.md.j2` |

## Default hooks always loaded in our pipeline

- `ssl_pinning_bypass.js`
- `jailbreak_bypass.js`
- `url_session_tracer.js`
- `commoncrypto_tracer.js`

See `frida_layer/auto_hook.py` for the decision logic that adds more.

## When to use this skill vs writing a one-off

- **Use this skill** for a sustained engagement where you want findings, correlation, and reports.
- **Use the upstream skill standalone** when you just want to grab a key from a binary and don't need the rest of the pipeline. The upstream `agent.py` is a great quick-start.
