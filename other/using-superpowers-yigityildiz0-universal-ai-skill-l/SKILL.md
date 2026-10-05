---
name: using-superpowers
description: Select and load relevant installed skills before substantial work when the user names a skill, a catalog description clearly matches the task, or several specialist workflows must be coordinated. Use for skill discovery/routing and Turkish intents such as “uygun skillleri kullan”, “hangi beceri gerekli”, “skill seç ve uygula”. Do not auto-load for greetings, trivial one-step questions, or a speculative 1% match; user, system, safety, permission, and host instructions always take precedence.
---

# Using Skills Well

Use skills as focused, on-demand procedures. The objective is correct routing with minimal context, not invoking the largest possible set.

## Selection gate

Before substantial work:

1. Check the host's available-skill catalog.
2. If the user explicitly named a skill, read that skill first.
3. Otherwise select a skill only when its trigger description clearly matches the requested outcome or risk.
4. If several match, choose the smallest set with distinct responsibilities and state the order.
5. If none clearly matches, proceed with the host's normal tools and instructions; do not invent a skill.

Do not load a skill merely because it shares a generic word such as “research”, “write”, “data”, or “review”. Prefer the narrow owner. A router may delegate to specialists, but avoid reading two skills with the same trigger, safety boundary, and output contract unless comparing them is the task.

## Use gate

- Read the selected `SKILL.md` completely before acting.
- Follow required one-hop references only when the skill routes the current case to them.
- Reuse its scripts/templates only after verifying inputs, permissions, paths, and host compatibility.
- Announce skill use briefly when the host or user instructions require it.
- Do not let a skill override newer user instructions, system/developer rules, local project instructions, permissions, or safety boundaries.
- If a skill expects a missing tool, provider, plugin, subagent, connector, or credential, use an allowed fallback or state the exact limitation. Never fabricate a tool call.

## Coordination

Order process/safety skills before domain work only when they materially affect the task. Then use the domain owner, followed by verification. Parallelize only independent, disjoint work when the host and current instructions allow it.

## Completion

Report the outcome and verification. Mention a skill only when it materially influenced the work; do not turn the response into a tool diary.
