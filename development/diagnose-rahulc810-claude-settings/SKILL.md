---
name: diagnose
description: Evidence-based debugging discipline for measurable systems. Trigger on:- diagnose, debug, why is X failing, what's causing, find the bug, root cause, investigate.
model: claude-opus-5
argument-hint: "target: local | server (default: local)"
allowed-tools: Read, Grep, Glob, Bash
---

# Diagnose

Not a pipeline stage — a stance to hold whenever something breaks. If a spec/plan is in
play, `.specify/memory/constitution.md` has the map; fixes found here are out of scope
(hand them to `plan-doc` or `implement`).

Before concluding a cause: get direct evidence for it (a log line, an independent repro, a timestamp), not just a story that fits. If symptoms don't unify under one cause, don't force them to — split and treat separately. Hold conclusions loosely enough to revisit if new evidence contradicts them, even ones already "ruled out."

## Target

- `local` (default) — investigate on this machine directly.
- `server` — investigate over SSH. Follow `/home/rahul/Documents/code/claude_settings/policies/ssh-policy.md`: read-only investigation
  only; any fix or change found along the way needs separate confirmation and is out of
  scope for this skill.

If the argument is omitted and it's ambiguous where the evidence lives (e.g. "the app is
slow" could be either), ask once before proceeding rather than guessing.