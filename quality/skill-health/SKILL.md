---
name: skill-health
description: "Diagnose and repair the TOS ecosystem itself. Use to check ecosystem health (every skill + shared engine), explain why something is failing by reading the audit trail (Quality Ledger, saved runtime execution traces, minority reports), find which files must change when a skill is added or renamed, and produce a human-readable repair plan you edit or approve. Trigger phrases: 'is the ecosystem healthy', 'why did this skill fail', 'audit the skills', 'diagnose the environment', 'what needs updating for the new skill', 'repair plan'. Runs shared/health/health.py (offline, stdlib). Do NOT use it to author lessons or assessments, or to score a single classroom artifact (that is quality-review) — this skill governs the system, not classroom artifacts."
---

# skill-health

Keeps the ecosystem healthy and consistent, and turns failures into repair plans a human can act on. It
governs the **system**, not classroom artifacts. Engine: `shared/health/health.py` (offline, stdlib);
canonical prose: `shared/health/health-model.md`.

## What it does
- **Scan readiness** — sweep every skill (name, `MAINTAINER.md`, synced references, evals, routing
  membership) + every shared engine (importable) + routing integrity; emit a readiness score + band,
  blocking issues, and a release-gate recommendation (doctor-style).
- **Diagnose** — read the audit trail (`ledger/ledger.json`; optional saved traces / decision records)
  and summarize recurring problems in plain language: validation failures, connector failure classes
  (PERMISSION / NOT_FOUND / DEGRADED_SUCCESS), and minority reports.
- **Impact analysis** — when a skill is added/renamed, list every ecosystem file that must update
  (`shared/routing/routing.json`, `ROUTING_MODEL.md`, `skills/core/teacher-core/references/routing-map.md`,
  `STATE.md`, `METRICS.md`, `shared/ontology/artifact-types.json`) so docs/routing/ontology never drift.
- **Repair plan** — an ordered, severity-tagged plan (each step marked mechanical or judgment) that you
  **edit or approve**; nothing high-stakes is auto-applied.
- **Apply (guided)** — `tools/skill_repair.py` consumes the approved plan, prints a plain-language
  approval summary, and on `--apply` performs only the **safe mechanical** fixes (regenerate derived
  files; re-run the drift guard); judgment items always stay with you.
- **Validate outputs** — `tools/validate_outputs.py` checks a governed artifact against its JSON Schema
  plus a governance / no-fabrication / no-real-PII rule catalog before it ships, and can promote a
  failing case into a regression eval.

## How it works — the unified pipeline
Follow `references/method.md` (`Request → Routing → Protocol Enforcement → Generation → Validation →
Quality Gates → Approval/Certification → Release`). Here Generation is the diagnostic pass:
`Analysis (scan) → Evidence (audit trail) → Diagnosis → Repair plan`. The plan is **advisory**: a human
approves edits, then re-run `tools/sync_check.py` and self-check against `references/quality-gates.md`
before handing to `quality-review`. When interpretations conflict, emit a minority report via the
canonical resolver (`shared/context/minority-report.md`).

```bash
python3 shared/health/health.py --summary
python3 shared/health/health.py --impact some-skill
python3 shared/health/health.py --diagnose --traces runtime/traces
python3 tools/skill_repair.py            # dry-run; --apply does safe mechanical fixes only
python3 tools/validate_outputs.py --input artifact.json --schema records
```

## Artifacts
See `references/artifact-types.md` — the **health report**, the **diagnosis**, and the **repair plan**.

## Output: always emit the metadata block
Every report ends with the metadata block from `references/metadata-schema.md` and
`human_review_required: true` — diagnostics and repair plans are decision support, not automatic changes.
No real student data; placeholders only.
