---
name: exec-cockpit
description: Template skill for a leadership-transition / executive cockpit — when someone steps into or covers a leadership role and needs to not drop anything. Produces a handoff doc + decision-rights map, an "open loops" tracker, a team-comms cadence, and a recurring report/update drafter. Trigger on "/exec-cockpit", "handoff doc", "decision-rights map", "open loops tracker", "cover for <role>", "interim <role>". Customize the placeholders to your situation.
---

# Exec cockpit (template)

Keeps a leadership role from crushing the person holding it. Four sub-deliverables — **drafts only for anything external; the human sends** (guardrail).

## 1. Handoff doc + decision-rights map  *(do first)*
One page, agreed with the outgoing leader before they leave. **Output: HTML** styled with `brand-assets/` (via `tools/render_brand_html.py`). Decision rights: what you decide alone vs. escalate (major spend, hiring/firing, board-level, anything structural).

## 2. "Open loops" tracker
Every thread the outgoing leader holds that could drop (key relationships, partner deals, board/investor threads). Status + next touch + owner. Refresh weekly.

## 3. Team-comms cadence
Set the recurring update rhythm (e.g. weekly all-hands). Prep agenda + talking points so the team feels led; draft the async recap (internal send ok; nothing external without approval).

## 4. Recurring report drafter
The periodic update you owe (board/investor/leadership). Pull live numbers at draft time; **persist none to git**; reproduce your branded layout. **Draft only — never auto-send.** See `references/sops/wf-investor-update.md`.

## Guardrails
All of `CLAUDE.md`. Especially: no confidential figures in the repo, draft-never-send external, cite-don't-invent. Needs `brand-assets/` filled for branded HTML output.
