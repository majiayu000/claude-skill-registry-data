---
name: learning
description: >-
  Turns a repeated mistake or correction into the smallest lasting fix (CLAUDE.md line, rule, hook) and prunes stale rules. Use when the user says you keep doing X, wants a rule for this project, or asks to clean up CLAUDE.md. Proposes first.
license: Apache-2.0
metadata:
  level: "setup"
  uses: ""
  agents: ""
  tokens: "740"
---

Finds what this session taught about the project, puts each lesson in the smallest layer that fixes it, and removes rules that no longer earn their place. Propose, then write after the user's ok.

## Steps
1. *Always.* Collect evidence from this session and `$ARGUMENTS`: a user correction, the same failure twice, a task that took several attempts, a repeated workflow. No concrete event and no request to prune: say "nothing to learn" and stop.
2. Read what exists: the CLAUDE.md contract and rules, `.claude/rules/`, hooks in `.claude/settings*.json`, project skills in `.claude/skills/` (names and descriptions only), the decisions file. `grep` for the lesson's keywords first: one home per fact.
3. Gate each lesson; drop it if any answer is no: a concrete event backs it; the agent cannot infer it from the code; no rule or hook already covers it.
4. Pick the smallest layer that works: nothing (one-off) → a CLAUDE.md line (one sentence, "Claude gets this wrong: …") → a path rule in `.claude/rules/` → for a rule that must hold with no exceptions, a `permissions.deny` entry ("never touch this path") or a hook (Bash hooks block, Write/Edit hooks only warn) → a project skill (a recurring multi-step procedure only). A change bigger than that: add a `proposed` entry to the decisions file and name `/foma-skills:groundwork` or foma-skills:shaping; do not do it here.
5. Prune in the same pass: rules naming files, commands or tools that no longer exist (check with grep), duplicates, contradictions, prose a hook already enforces, rules that failed to prevent a repeat (escalate one layer or delete), stamps older than 90 days. CLAUDE.md over 200 lines: one in, one out.
   If `.scratch/fires.jsonl` exists, count sessions as distinct session ids on its `"event":"start"` rows. At 20 or more, pack skills with no fire row in that log become one proposal (names and the session count; the user disables or keeps them). Under 20: say the log is too short and propose nothing from it.
6. Present at most 3 proposals: evidence, layer, the exact diff (removed lines quoted), what it removes. Ask per item; write only approved ones; end new rule lines with the date `(YYYY-MM-DD)` so the next run can re-check them.
7. A new hook or project skill is kept only after one check: the hook on one input that must trigger it and one that must not; the skill on one prompt that must fire it.

## Rules
- Never edit foma-skills files (a plugin update overwrites them): a gap in the pack becomes a project rule and a suggested upstream issue text.
- Never write without an ok per item; never log in the background.
- Never add what the code or git history already shows, or a general best practice.
- A lesson with no evidence is not written; ask the user for the event instead.
- Never raise the layer without need: a hook for a one-time slip is over-engineering.

## Report
- Proposals: written / declined, each with its layer; pruned lines.
- Not checked: <…>
