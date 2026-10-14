---
name: attention-triage
type: Skill
title: "attention-triage — keep the owner's attention card short and worth reading"
description: "The runbook a triage agent follows on each run over the super-admin attention dock, through the attention MCP tool. Use when a scheduled attention-triage routine wakes, when asked to triage, clean up or shrink the attention dock or admin alerts, or when the dock's card is over budget."
tags: [attention, triage, admin, routines]
timestamp: 2026-10-11T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/attention-triage/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# attention-triage

Arman, 2026-10-11: "they bombard me so the important things get missed ... I stop looking, and
eventually I turn the feature off." Your job is the opposite: every run leaves his card with only
ready decisions, at most the budget (knob `platform.attention.card_budget`, default 5).

**Model.** Plumbing, not intelligence: run the routine on the cheapest capable model (Haiku for a
Claude routine; a platform agent uses `agent_catalog action=test_model purpose=plumbing`, see
the test-model-selection skill). Escalate to a stronger model only to fix a cause in code.

**Cadence.** Three times a day (08:00, 13:00, 18:00 Pacific). Claim the window first:
`schedule_claim` with task_key `attention-triage`; `already_claimed_by` means stop.

**Tool.** `attention` on the AI Dream MCP (admins only). Audience, readiness and the budget are
decided by the database (`platform.attention_card`), the same rules the dock uses. Every write
needs a note and is audited.

## Each run

1. **List.** `attention action=list`. Read `summary` (on card, budget, over budget, being prepared)
   and each item's `audience`, `routed_to`, `readiness.reason`, `age_hours`, `recurring`, `links`.
2. **Fix what is fixable, or file it.** For each `agent_fix` item: open its evidence link, fix the
   cause if it is small and in your reach, then `resolve` with what you changed. Otherwise
   `file_to_agents` with a one-line note of what to do; it creates or updates one work-loop item
   per dock item (campaign `attention-triage`).
3. **Resolve stale items.** An item with no new occurrence for the stale window and not recurring:
   `resolve` with "stale: <why it no longer matters>". It comes back by itself if it happens again.
4. **Merge duplicates.** Two items about the same cause: keep the clearest, `resolve` the others
   with "duplicate of <title>".
5. **Make owner decisions ready.** For each `owner_decision` that failed readiness, `escalate` it
   with what it lacks: `sentence` (one plain sentence, no ids or codes, under 220 characters),
   `recommended_action` (the ONE click: approve, reenable, open_held_run, ...) and `consequence`
   (what that click does). A refusal names the reason; fix it or file it. If it is not truly his
   call, `reclassify` it (or its whole kind, `scope=kind`) to `agent_fix` or `info_only` with a
   reason. Standing rules: a hold on a general-purpose agent (General Chat and the like) is
   `agent_fix` (give the mandate a dedicated agent through the factory); a limit hit on a system
   job is `agent_fix`.
6. **Keep the card within budget.** If `summary.over_budget > 0`, `list` already filed the
   "card over budget" work item; resolve, merge or reclassify until `owner_ready` is at most the
   budget.
7. **Leave one line.** End with a single sentence: what you fixed, filed, resolved, and what is
   left on his card, e.g. "Fixed 2, filed 5, resolved 3 stale; 1 decision left for Arman (approve
   the weekly digest spend)."

`attention action=report days=7` shows what reached him, what he acted on, the signal rate per
kind, and audience changes (including auto-demotions: a kind he mutes or ignores twice without
acting moves to agents). A kind with a low signal rate is a kind to fix or reclassify, not to
show again.

## Never

- Never escalate to make the card look busy; an empty card is the goal.
- Never mute instead of fixing; a mute is his tool, not yours.
- Never put ids, codes or stack text in a sentence for him.
