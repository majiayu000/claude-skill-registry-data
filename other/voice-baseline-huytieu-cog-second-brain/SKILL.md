---
name: voice-baseline
description: Measure your own writing corpus for the words and sentence shapes you over-use, so an agent writing in your voice stops amplifying your tics into a style. Produces a counted baseline file and checks any new draft against it. Use when an agent's drafts start sounding like a caricature of you, before publishing anything written in your voice, or every ten new pieces to re-measure.
---

Read `.claude/skills/voice-baseline/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
