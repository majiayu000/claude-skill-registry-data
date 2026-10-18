---
name: ask-xeno
description: The top of this library. Ask it which family your task belongs to, then take the family's own route from there. Reach for it when you are unsure which skill applies, when a task spans families, or when you suspect a skill exists for this and cannot name it. Deliberately thin — it names the family entries and nothing else, so it stays cheap enough to carry everywhere. Triggers include "is there a skill for X", "which skill should I use", "how do we do X here", and any moment you are about to improvise a process this library already encodes.
---

# Ask Xeno

**The entries. Pick one and follow its route — the detail lives there, not here.**

| You are… | Enter at |
|---|---|
| **Working in a T4 repo** — building a feature, filing an issue or PR, recording a decision, picking up where a session left off, running unattended, or writing anything the developer reads | **`using-t4`** |
| **Handing work to another agent** — executing a scoped subtask, convening a panel for judgment, or hunting a bug across agents | **`using-clink`** |
| **Designing a web UI** — prototyping, micro-UI rules, auditing, layout reasoning | **`using-design`**; anti-slop **`using-anti-slop`**; 3D/motion **`using-web3d`** |
| **Writing code, in any repo** | **`karpathy-guidelines`** — simplest thing that works, surgical diffs, verifiable success criteria |
| **Auditing a codebase for vulnerabilities** — a full security audit or pen-test | **`using-security-audit`** — Cloudflare's skill, installed on demand |
| **Running as Qwen3.8** (27B or Flash-Next) — the session's model is the local Qwen, through Claude Code | **`using-qwen38`** — the map from task to skill to gate (`qwen38-think` first, `qwen38-claude-code` before the first tool call, then `design-ship-gate` or `qwen38-code-gate`), and the four rules that model needs written down |
| **Writing a skill for Qwen3.8** — a skill a small, literal model will follow | **`qwen38-skill-style`** — enumerate, command + pass condition, fixed done-report, one with/without pair |

**This file stays thin on purpose.** Each family entry already carries its own map and its own rules; restating them here would create a second copy that drifts from the first. If you find yourself wanting to add detail to this table, it belongs in the family entry instead.

**When nothing here fits**, say so and use the general skills directly. A skill invoked because it was the nearest one is worse than none — it makes the wrong process look chosen.
