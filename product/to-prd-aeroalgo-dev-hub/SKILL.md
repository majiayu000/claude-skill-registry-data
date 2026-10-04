---
name: to-prd
description: "Alias for to-spec — synthesize conversation into a structured product/spec doc without new interview questions. Use when user says to-prd or wants a PRD after grilling/clarify."
disable-model-invocation: true
---

# to-prd (hub alias)

Upstream Matt Pocock renamed **to-prd → to-spec**. This skill is a thin alias.

**Do this:** Read and follow `.agents/skills/to-spec/SKILL.md` entirely.

Hub adaptation for PLAN/CLARIFY:
- Prefer writing under `memory-bank/{role}/plan/<epic_id>/md/` or a path the user names — do **not** require external issue tracker if unset.
- If tracker setup is missing, synthesize the spec to disk and report the path; do not block on `/setup-matt-pocock-skills`.
- **FORBIDDEN:** start a new interview; this is synthesis-only after clarify/grill is done.
