---
name: eris-solver-rules
description: Use when solving, planning, reviewing, or debugging Project Eris challenge submissions, Kaggle/Eris solver scripts, challenge-specific "What Not To Use" rules, offline Kaggle Docker constraints, leaderboard/OOF strategy, reviewer warnings, rulebook changes, or requests to audit whether an Eris solution follows the Project Eris Solver Guidebook.
---

# Eris Solver Rules

## Core Workflow

1. Read the challenge statement first, especially any "What Not To Use", "Not Intended Approaches", runtime, model, data, internet, or submission-format restrictions.
2. Read [references/guidebook-checklist.md](references/guidebook-checklist.md) before planning or coding an Eris solution.
3. If the user provides local rule files such as `p1.txt`, `p3.txt`, challenge notes, reviewer feedback, or a newer guidebook link, read those too.
4. Follow the strictest applicable rule when the guidebook, challenge statement, and user/local rules differ. Challenge-specific rules override the guidebook when they are real restrictions; user rules can be stricter than both.
5. For any solution plan or script, explicitly audit data use, libraries, training location, test-set usage, runtime, submission shape, and domain-specific compliance.

## Maintenance

When a new rule, warning, reviewer comment, platform behavior, or recurring failure appears:

1. Update [references/update-log.md](references/update-log.md) with date, source, issue, required behavior, and preventive check.
2. If the rule affects future solver behavior, also update [references/guidebook-checklist.md](references/guidebook-checklist.md).
3. Keep entries concise and operational. Prefer "what to check or do" over long narrative.
4. Do not delete older warnings unless they are explicitly superseded. Mark superseded items and state the replacement rule.
5. If a source link is provided, record it. If the rule is inferred from a reviewer comment, say so.

## Compliance Answer Pattern

When asked whether a plan or script follows the rules:

1. State `Compliant`, `Mostly compliant`, or `Not compliant`.
2. List only concrete blockers and fixes.
3. Mention any grey-area items that could be rejected even if technically allowed.
4. Confirm the exact challenge-specific prohibitions were respected.
5. For CV tasks, verify a real trained CV model is central, not a tabular/rule-only substitute.
6. For any task, verify all training/fine-tuning happens inside the submitted script unless the task explicitly says otherwise.

## Source Of Truth

Primary external guidebook:

`https://docs.google.com/document/d/1PtOMRY1_uuk_yUOHjiBWfcCipHCQ9s1KIqp_Wj3o_GU/edit?tab=t.0`

Use the export endpoint for refreshes when accessible:

`https://docs.google.com/document/d/1PtOMRY1_uuk_yUOHjiBWfcCipHCQ9s1KIqp_Wj3o_GU/export?format=txt`

Current local distilled reference was created from the guidebook on 2026-07-10.
