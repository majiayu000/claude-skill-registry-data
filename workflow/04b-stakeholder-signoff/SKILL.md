---
name: 04b-stakeholder-signoff
description: >
  Use after evaluation (Step 4) passes but BEFORE deployment (Step 6). Covers
  translating technical eval metrics to business-meaningful terms, running a
  structured review with business and compliance stakeholders, capturing
  sign-off, and blocking promotion if review-blocking issues remain. Mirrors
  the "Align with stakeholders before production" phase of the Databricks
  agents development workflow. SDLC Step 4b. Do NOT use this skill in place
  of Step 4 eval — this is the gate layered on top of it.
license: Apache-2.0
compatibility: "Works with any Databricks workspace. Uses MLflow Evaluation UI and (optionally) Review App labeling sessions."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Stakeholder sign-off is a review process (MLflow Evaluation UI / Review App) — no deployed resource and no client-specific mechanics. Identical on both clients. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-04-15"
  volatility: medium
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.2.0"
  domain: "genai-agents"
  pipeline_position: "S4b"
  consumes: "evaluation_run, held_out_dataset, scorer_definitions"
  produces: "signoff_artifact, business_metrics_report, deployment_gate"
  grounded_in: "https://docs.databricks.com/aws/en/generative-ai/guide/agents-dev-workflow"
fields_read:
  - governance.monitoring.rollback_trigger_example
---

# Stakeholder Sign-Off Gate

The Databricks agents development workflow has five phases: Understand, Build, Iterate on quality, **Align with stakeholders**, Release & Monitor. This skill covers the fourth phase — the gate that turns a technically-good agent into a business-approved release.

Engineering-only gates fail in the field. A scorer-pass-rate of 0.92 is meaningless to a compliance officer, a product manager, or a support lead. Sign-off bridges that gap.

---

## When to Use

- Your Step 4 evaluation run is green against all hard thresholds.
- You are about to request a production deployment (Step 6).
- You have ≥ 1 non-engineering stakeholder (PM, compliance, domain SME, support lead) who owns outcomes the agent affects.

Skip **only** if the agent is a purely internal developer tool with no external user impact.

---

## Sign-Off Deliverables

Produce each item below. Store them under the **versioned signoff path** so releases are auditable.

### Versioned Resource Path Contract

Every persisted workshop artifact that can be superseded must be versioned. This skill is responsible for the **signoff** artifact under that contract:

- signoffs: `/Volumes/<catalog>/<schema>/signoffs/v<N>/decision.md`
- eval summaries: `/Volumes/<catalog>/<schema>/eval_runs/v<N>/summary.json` (produced by [`04-evaluation-runs`](../04-evaluation-runs/SKILL.md))
- prompt candidates: `prompts:/{catalog}.{uc_agent_schema}.system_instructions@candidate_v<N>` (produced by [`01-prompt-registry`](../01-prompt-registry/SKILL.md) / [`08b-prompt-handauthoring`](../08b-prompt-handauthoring/SKILL.md))
- deployment plans: `/Volumes/<catalog>/<schema>/deployment_plans/v<N>/plan.md` (produced by [`06-deployment-and-automation`](../06-deployment-and-automation/SKILL.md))

`<N>` is a monotonically increasing integer per artifact type, scoped to `(catalog, schema, artifact_type)`. Resolve `<catalog>` and `<schema>` from the live state file (`<catalog>` is the bundle catalog, `<schema>` is the ops schema, e.g. `skyloyalty_ops`). Never overwrite an existing `v<N>` — always write a fresh `v<N+1>`. The deployment skill's CI gate, monitoring rollbacks, and retros all index off these paths, so omitting the `v<N>` segment silently breaks downstream traceability.

### 1. Business Metrics Report (1 page)

Translate technical metrics to business-meaningful claims. Template:

```markdown
# SkyLoyalty Agent v12 — Business Metrics Report

## What the agent will do in production
One-paragraph description, in business terms, of the user-visible behavior
(not the architecture).

## How well it does it — based on a held-out 50-row sample

| Business claim | Technical scorer | Target | Result |
|---------------|------------------|--------|--------|
| "Cites the right policy page" | `source_citation_scorer` | ≥ 0.95 | 0.98 |
| "Follows SkyLoyalty tone guidelines" | `tone_judge` | ≥ 0.90 | 0.94 |
| "Handles edge-case tier rules correctly" | `domain_accuracy_judge` | ≥ 0.85 | 0.91 |
| "Never books an award without confirmation" | custom rule | 100% | 100% |

## Where it still fails
- 3 rows misidentified SKY-POL-008 vs SKY-POL-009. Risk: medium.
- 1 row refused a legitimate request. Risk: low.

## Changes since v11
- Prompt v7 → v8 (source citation improvements from optimization run).
- New policy docs indexed in vector store.

## Expected user impact
- ~450 turns/day based on current pilot traffic.
- Estimated +8% containment vs v11 baseline.
```

### 2. Failure Mode Walkthrough (live or recorded)

Walk stakeholders through **5 real failing rows** and **5 real passing rows** from the eval set. Prefer live over async — questions catch issues no report surfaces.

### 3. Compliance / Risk Checklist

One-page checklist with binary answers. Example:

| Item | Evidence | Status |
|------|----------|--------|
| PII never leaves the agent boundary | Gateway guardrails + 20-row audit | ✓ |
| Agent refuses requests outside policy scope | `valid_topics` + 10-row audit | ✓ |
| Rollback plan in place | Alias revert procedure in runbook | ✓ |
| Monitoring in place with on-call | Scorer + alert wired | ✓ |
| Review-app labeling cadence agreed | Weekly, 20 traces | ✓ |

### 4. Decision Record

Capture the **decision**, not just the metrics. The decision MUST be machine-readable. Use a YAML front-matter block at the top of `decision.md`; free-form prose may follow but is **never** consulted by the CI gate.

```markdown
---
engineering_signoff:
  decision: APPROVED            # one of: APPROVED | REJECTED | APPROVED_WITH_CONDITIONS
  owner: eng-lead@example.com
  approved_at: "2026-04-26T00:00:00Z"
  conditions: []
  rejection_reason: ""
stakeholder_signoff:
  decision: APPROVED            # one of: APPROVED | REJECTED | APPROVED_WITH_CONDITIONS
  owner: pm@example.com
  approved_at: "2026-04-26T00:00:00Z"
  conditions:
    - "Monitor citation score daily for 2 weeks"
  rejection_reason: ""
rollback_trigger: "citation_scorer < 0.90 over 24h window"
next_review: "2026-05-03"
---

# Decision: Promote SkyLoyalty Agent v12 to production

Deciders: PM (J. Park), Compliance (R. Diaz), Eng lead (S. Kim).
Optional human-readable narrative goes here. The CI gate ignores this body
and parses only the YAML front matter above.
```

Two **separate** signoff blocks are required:

- `engineering_signoff` — owned by the eng lead. Confirms the candidate passes hard thresholds, that rollback wiring is real, and that no known regressions are masked.
- `stakeholder_signoff` — owned by the business / compliance / PM side. Confirms the business-metrics translation, the failure-mode walkthrough, and any conditions.

Both blocks must reach `decision: APPROVED` (or `APPROVED_WITH_CONDITIONS` with explicit conditions captured) for production registration to proceed. If either block is `REJECTED`, the gate blocks; the `rejection_reason` field is the audit record.

Store as markdown in the signoff volume at `/Volumes/<catalog>/<schema>/signoffs/v<N>/decision.md`; reference the path from the deployment PR.

> **Substring grep is forbidden.** Do not parse `decision.md` with `grep "APPROVED"` or `"Decision: APPROVED" in text`. The narrative body of the file may legitimately contain phrases like "the previous v11 was APPROVED" or quote rejection reasons that mention the word APPROVED; substring matching is unreliable and trivially bypassed. Always parse the YAML front matter and read the typed `decision` enum.

---

## The Sign-Off Meeting

Keep it to 45 minutes. Structure:

1. **(5 min)** Business metrics recap — read the one-pager.
2. **(20 min)** Live failure walkthrough — 5 fail + 5 pass from eval set.
3. **(10 min)** Risk checklist — stakeholders sign or object.
4. **(10 min)** Decision + conditions + rollback trigger.

Do **not** use this meeting to re-debate thresholds. If a stakeholder wants tighter thresholds, that is a new Step 4 iteration, not a sign-off blocker.

---

## Blocking the Deployment

Until sign-off is captured, CI must block promotion. Enforce mechanically by **parsing the YAML front matter** — never substring-grepping the markdown body.

```python
# In your promotion script (called from CI)
from pathlib import Path
import yaml

ALLOWED = {"APPROVED", "APPROVED_WITH_CONDITIONS"}

# Resolve <catalog>, <schema>, and <version> from state — never hard-code.
# Path contract: /Volumes/<catalog>/<schema>/signoffs/v<N>/decision.md
signoff_path = Path(f"/Volumes/{catalog}/{schema}/signoffs") / f"v{version}" / "decision.md"
if not signoff_path.exists():
    raise SystemExit(
        f"Blocked: no signoff at {signoff_path}. Run the signoff workflow before promoting."
    )

text = signoff_path.read_text()
if not text.startswith("---\n"):
    raise SystemExit(f"Blocked: signoff is missing YAML front matter at {signoff_path}.")
_, front, _ = text.split("---\n", 2)
meta = yaml.safe_load(front) or {}

eng = (meta.get("engineering_signoff") or {})
biz = (meta.get("stakeholder_signoff") or {})
eng_decision = eng.get("decision")
biz_decision = biz.get("decision")

if eng_decision not in ALLOWED or biz_decision not in ALLOWED:
    # state_override is the single audit-tracked escape hatch. It MUST capture
    # the original decision verbatim (so the override can be reviewed).
    override = meta.get("state_override") or {}
    captured_eng = (override.get("engineering_signoff") or {}).get("decision")
    captured_biz = (override.get("stakeholder_signoff") or {}).get("decision")
    if captured_eng != eng_decision or captured_biz != biz_decision:
        raise SystemExit(
            "Blocked: signoff not APPROVED and no state_override captures "
            f"the original decisions (eng={eng_decision}, stakeholder={biz_decision})."
        )
```

Reject PRs that bypass this check. The signoff artifact is part of the release; deploying without it is a compliance gap. The `state_override` block is the **only** way to bypass a non-APPROVED decision, and it must record the original decisions for audit.

> **Substring grep is forbidden.** Anything that does `if "APPROVED" in decision_text` or `grep -q APPROVED decision.md` is a bug — narrative bodies legitimately contain those words. Parse the typed YAML enums.

---

## Integrating With MLflow

Reference the exact MLflow evaluation run URL in the business metrics report. This lets stakeholders drill into any row they want to see in detail:

```markdown
Eval run: https://<workspace>.cloud.databricks.com/ml/experiments/<exp-id>/runs/<run-id>

Dataset:  main.skyloyalty.skyloyalty_agent_benchmarks (version 12)
Scorers:  source_citation_scorer, tone_judge, domain_accuracy_judge
Held-out split: 50 rows (20% of total)
```

If you used an MLflow labeling session for human spot-checks, reference its URL too.

---

## Rolling Forward After Deployment

The sign-off is not a one-shot event. Recurring cadence:

- **Weekly** — review production monitoring (see [07-production-monitoring](../07-production-monitoring/SKILL.md)) with same stakeholders; record short notes.
- **Per incident** — if the rollback trigger fires, revert alias, re-run signoff on the fix.
- **Quarterly** — re-label a 50-row sample via MLflow review app; refresh business metrics report.

---

## Do's and Don'ts

|  | Do | Don't |
|---|---|---|
| **Metrics framing** | Translate to business claims ("cites right doc 98% of the time"). | Show raw scorer names with no context. |
| **Meeting** | Walk through real failing rows. | Present only summary statistics. |
| **Decision** | Capture name, date, conditions, rollback trigger. | Let the approval live in a Slack reaction. |
| **CI gate** | Block deploy on signoff artifact presence + approval text. | Rely on trust that signoff happened. |
| **Cadence** | Weekly monitoring review with same humans. | One-and-done review. |
| **Rejections** | Loop back to Step 3/4 with concrete new thresholds. | Treat a rejection as a Step 6 problem. |

---

## Validation Checklist

- [ ] Held-out eval split (not the same split used for optimization) passes all hard thresholds.
- [ ] Business metrics report written and shared 24h before the review meeting.
- [ ] 5 failing + 5 passing rows from the eval run selected for live walkthrough.
- [ ] Compliance / risk checklist signed.
- [ ] Decision record committed to the versioned UC volume path `/Volumes/<catalog>/<schema>/signoffs/v<N>/decision.md`. YAML front matter parses cleanly; `engineering_signoff.decision: APPROVED` (or `APPROVED_WITH_CONDITIONS`) and `stakeholder_signoff.decision: APPROVED` (or `APPROVED_WITH_CONDITIONS`) — no substring grep on the narrative body.
- [ ] Rollback trigger defined and wired to a monitoring alert.
- [ ] CI promotion script verifies signoff artifact before running `databricks bundle deploy`.
- [ ] Next review date on the team calendar.

---

## References

### Official documentation

- [Databricks agents development workflow](https://docs.databricks.com/aws/en/generative-ai/guide/agents-dev-workflow) (five-phase lifecycle)
- [MLflow evaluation runs](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs)

### Related skills

[04-evaluation-runs](../04-evaluation-runs/SKILL.md) · [06-deployment-and-automation](../06-deployment-and-automation/SKILL.md) · [07-production-monitoring](../07-production-monitoring/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-04-26 | Decision Record now requires structured YAML front matter with `engineering_signoff` + `stakeholder_signoff` blocks (each carrying typed `decision` enum, owner, conditions, rejection_reason). CI gate parses YAML and forbids substring grep; production registration is blocked unless both decisions are `APPROVED`/`APPROVED_WITH_CONDITIONS` or a `state_override` captures the original decision. |
| 1.1.0 | 2026-04-26 | Added Versioned Resource Path Contract section; normalized signoff path to `/Volumes/<catalog>/<schema>/signoffs/v<N>/decision.md`; CI snippet now resolves catalog/schema from state instead of hard-coding `main/skyloyalty_ops`. |
| 1.0.0 | 2026-04-19 | Initial skill: sign-off artifacts, meeting structure, CI gate, MLflow integration, rolling cadence. |
