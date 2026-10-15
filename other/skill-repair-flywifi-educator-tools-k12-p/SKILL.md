---
name: skill-repair
description: "Apply an APPROVED skill-health repair plan with the smallest durable change. Use after skill-health (or a human) has diagnosed an issue and you want it fixed: it separates mechanical fixes (safe to automate) from judgment fixes (human-only), shows a plain-language approval summary, and on approval applies ONLY the safe mechanical fixes then re-runs the drift guard. Trigger phrases: 'apply the repair plan', 'fix the broken skill', 'patch this skill', 'run the approved fixes'. Runs tools/skill_repair.py (stdlib, so it always runs). Do NOT use it to diagnose (that is skill-health) or to redesign a skill — it makes the minimum change, preserves untouched behavior, and keeps approval explicit."
---

# skill-repair

Repairs a skill carefully: **tight scope, smallest stable fix, explicit approval trail.** It never
silently expands a narrow fix into a redesign. Engine: `tools/skill_repair.py` (stdlib, always runs);
diagnosis comes from **skill-health** (`shared/health/`).

Follow the unified pipeline (`references/method.md`); the repair work is the Generation stage
(`Analysis (read the approved plan) → Patch (smallest fix) → Validation → Approval`).

## Workflow (`references/patch-principles.md`)
1. **Confirm the basis** — prefer an approved plan from `skill-health`; if none, produce a short
   diagnosis + proposed changes and **stop for approval** first.
2. **Prepare** — read the full skill before editing; identify only the files that truly need changes;
   preserve untouched behavior; snapshot before replacing anything.
3. **Patch minimally** — separate **mechanical** (safe to automate) from **judgment** (human-only); fix
   the root cause, not the symptom; prefer simplifying fragile logic over adding complexity.
4. **Validate** (`references/validation-checklist.md`) — re-run `tools/sync_check.py`, re-read changed
   files, and explicitly call out anything that could not be tested.
5. **Summarize for approval** (`references/approval-summary-template.md`) — plain language: what changed,
   why, what stayed the same, and any risk. **Stop for approval before finalizing.**

## Safety rules
- **Dry-run by default**; `--apply` performs ONLY safe mechanical fixes (regenerate derived files; re-run
  the drift guard). Judgment items always stay with the human.
- Prefer official documentation over forum advice. If the real problem is **broad architectural drift**,
  say so and recommend a larger refactor — don't hide it inside a "small patch."
- Never present a patch as complete if the risky parts could not be validated.

## Output: always emit the metadata block
End with the metadata block (`references/metadata-schema.md`) + `human_review_required: true`. When a fix
needs judgment, route it back to the owning skill / a human. Placeholders only; never real student data.

```bash
python3 tools/skill_repair.py            # dry-run: what would change, what needs you
python3 tools/skill_repair.py --apply    # safe mechanical fixes only, then re-run sync_check
```
