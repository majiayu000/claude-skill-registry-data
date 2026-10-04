---
model_tier: high
name: rule-refactor
description: "Use when the rule set is over the Augment budget, when a new rule would breach it, or when asked to audit / merge / prune rules — runs the audit pipeline and proposes a verdict per rule."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

<!-- cloud_safe: degrade -->

# rule-refactor

## When to use

* `measure_augment_budget --check` fails (utilisation ≥ 0.95)
* A new rule would push the budget over 0.95 — caught by the budget
  gate in [`rule-writing`](../rule-writing/SKILL.md)
* User says "audit rules", "rule cleanup", "rules over budget",
  "prune rules", "merge rules", "rule system review"
* Periodic governance pass after a batch of rule additions

Do NOT use this skill for:

* Editing a single rule's content → [`rule-writing`](../rule-writing/SKILL.md)
* Picking always vs auto for one new rule → [`rule-writing`](../rule-writing/SKILL.md)

## Iron Law

**Threshold-lift is forbidden.** When the budget breaches, the
content must shrink — not the gate. Loosening `FAIL_THRESHOLD` in
`scripts/measure_augment_budget.ts` to make CI pass is an explicit
anti-pattern. The only valid budget-growth move is an ADR that
raises `TOTAL_CAP`.

## Procedure

### 1. Inspect the current budget state

```bash
./scripts-run src/scripts/measure_augment_budget --json > /tmp/budget-before.json
./scripts-run src/scripts/measure_rule_budget --json > /tmp/rule-budget-before.json
```

### 2. Run the audit pipeline

The audit infrastructure already exists — compose it:

```bash
./scripts-run src/scripts/audit_auto_rules      # → agents/runtime/reports/auto-rules-audit.{json,md}
./scripts-run src/scripts/audit_overlap         # → appends overlap pairs to the MD
./scripts-run src/scripts/audit_likelihood      # → agents/runtime/reports/auto-rules-likelihood.json
```

Then read `agents/runtime/reports/auto-rules-audit.md` end-to-end.

### 3. Categorise every flagged rule

For each rule the audit surfaces (overlap pair, low-likelihood, oversized,
or the new addition that triggered this skill), assign exactly one verdict:

| Verdict | Test |
|---|---|
| **keep** | Iron-Law / always-on safety net, no overlap, fires often |
| **merge** | ≥ 2 rules same domain, near-identical triggers, overlap ≥ 0.4 |
| **delete** | Never fires (low-likelihood + no path/keyword hit in 30 days), or fully subsumed by a skill |
| **move-to-context** | Body is reference material (tables, mechanics, examples) — the obligation is short, the rest is lookup |
| **promote-to-skill** | Body has numbered steps / a workflow — not a constraint |

### 4. Present the verdict table to the user

One Markdown table, one row per flagged rule, **before** any file
change. User approves the list. No silent edits.

### 5. Apply approved changes

For each approved verdict:

* **merge** → rewrite the surviving rule to cover both domains;
  delete the absorbed one; update any `routes_to:` references.
* **delete** → remove the file from `src/rules/`
  and the corresponding `dist/agent-src/rules/` projection.
* **move-to-context** → extract the body into
  `src/agent-src/contexts/<area>/<name>.md`, replace the
  rule body with the obligation + a `load_context:` pointer.
* **promote-to-skill** → create
  `src/skills/<name>/SKILL.md`, replace the rule
  with an auto-trigger stub that routes to it (or delete the rule
  entirely if the skill's own trigger suffices).

### 6. Re-validate

```bash
bash scripts/condense.sh --sync
./scripts-run src/scripts/condense --generate-tools
./scripts-run src/scripts/measure_augment_budget --check   # must exit 0
./scripts-run src/scripts/skill_linter --all               # 0 FAIL
```

Then run your package's full CI pipeline (see `Taskfile.yml` for the
canonical sequence) before pushing.

### 7. Record the delta

Append a snapshot to `agents/runtime/.augment-budget-history.jsonl`:

```bash
./scripts-run src/scripts/measure_augment_budget --trend-append
```

Commit the cleanup as a separate chunk from any rule-add commits so
the history shows "added X" + "cleaned up Y" as distinct steps.

## Output format

1. Verdict table (approved by user) at the top of the cleanup PR description
2. Per-verdict commits (one per merge / delete / move / promote group)
3. Final `measure_augment_budget --check` output showing utilisation < 0.95
4. Trend snapshot recorded

## Gotchas

* Do NOT raise `FAIL_THRESHOLD` to dodge the audit
* Do NOT delete a rule that has a `routes_to:` pointer without
  updating the pointer's source
* Do NOT merge rules across tier boundaries (e.g. tier-1 always
  with a tier-3 stub) without surfacing the tier collapse to the user
* Do NOT skip the trend-append — the history is what tells future
  agents how the cap was managed

## Do NOT

* Do NOT loosen the budget gate
* Do NOT touch the cap (`TOTAL_CAP`) without an ADR
* Do NOT apply changes before user approves the verdict table
* Do NOT delete the rule-refactor audit reports — they're the
  artifact reviewers cite

## Cloud Behavior

On cloud surfaces, the audit scripts are not reachable. The skill
still applies — prose-only:

* Inspect the rule list (frontmatter + descriptions) and propose the
  verdict table from reading alone.
* Tell the user to run the audit scripts locally before applying.
* Do not attempt to call any script.
