---
model_tier: medium
name: history-design
description: "Use when choosing HOW to record change history / audit trails — walks the tier matrix (columns → audit log → temporal → event sourcing). Triggers on 'wer hat was wann', 'audit log'."
domain: engineering
workspaces:
  - engineering
packs:
  - history-discipline
trust:
  level: professional
install:
  default: false
  removable: true
---

# history-design

## When to use

- A model/table is declared audit-scoped ("we need to know who changed
  what and when") and the mechanism must be chosen — NOT assumed.
- The user asks for an audit trail, change history, activity log, or
  proposes event sourcing.
- NOT for reviewing an existing migration diff (route to
  `schema-review`) and NOT for privacy/DSR policy design (route to
  `privacy-review`; this skill only wires the interlock).

## Procedure

1. **Collect the requirement facts** (ask ONE question only if missing):
   who edits the data (single editor vs multi-tenant), compliance need
   (GDPR/SOC2/audit), point-in-time query need, replay/projection need,
   expected mutation volume.
2. **Walk the tier matrix — normative, cheapest-sufficient wins:**

   | Tier | Mechanism | Use when | Growth control |
   |---|---|---|---|
   | 0 | `updated_at`/`updated_by` columns | single-editor, no compliance need | none needed |
   | 1 | Row-level audit log (Laravel: spatie/activitylog or owen-it/laravel-auditing; TS: thin custom audit table) | admin panels, SaaS tenant data, "wer hat was wann geändert" | retention policy REQUIRED | <!-- md-language-check: ignore -->
   | 2 | DB temporal/system-versioned tables | point-in-time queries needed, DB supports it | partition rotation |
   | 3 | Event sourcing | domain genuinely event-driven, replay/projection needed | snapshotting + archive REQUIRED |

   **Default tier: 1.** Tier 3 requires an explicit architecture waiver
   from the user — never "upgrade" to event sourcing unprompted.
3. **Apply the four interlocks to the chosen tier:**
   - **Hygiene (R-B3):** audit storage indexed on
     `(auditable_type, auditable_id, created_at)`; store JSON diffs, not
     full-row copies, where a diff suffices.
   - **Growth (R-A7):** the audit table itself declares retention (TTL,
     pruning job, partition rotation, or archive path) — history must
     not re-create the unbounded-growth problem it documents.
   - **Privacy (R-B4):** audit records inherit the deletion/
     anonymization obligations of the data they describe — a GDPR
     Art. 17 path must exist before the mechanism ships.
   - **Reliability (R-B5):** audit capture is same-transaction (Tier-1
     default: observer + cheap single insert — allowed request-path
     work) OR outbox/afterCommit with a durable queue when offloaded. A
     lossy audit trail is worse than none.
4. **Emit the decision artifact** (Output below) and, when the tier
   lands, hand implementation to the stack-native path (Laravel package
   install + config, or the thin custom audit-table pattern for TS — no
   dependency needed there).

## Output

The decision artifact MUST contain:

1. **Tier decision line** — `Tier N — <mechanism>` plus the one-sentence
   cheapest-sufficient justification.
2. **Interlock checklist** — the four interlocks (hygiene, growth,
   privacy, reliability) each with its concrete answer for this model,
   not a bare checkmark.
3. **Rejected-tier note** — one line on the nearest rejected tier and
   why (usually why NOT event sourcing, or why Tier 0 is insufficient).

## Gotcha

- Tier-1 reference per stack — Laravel: **spatie/laravel-activitylog**
  (source-level comparison 2026-07-27: age-based `activitylog:clean`
  retention command maps directly onto the R-A7 growth budget; JSON diff
  columns match R-B3 hygiene) with **owen-it/laravel-auditing** as the
  forensic alternative (ip/url/user-agent/tags; count-based pruning);
  TS/Node: the thin custom audit-table pattern, no dependency. Re-verify
  the package pick against the project's framework version at decision
  time.
- Tier 2 (temporal tables) depends on the database: MariaDB/SQL Server
  have system-versioned tables, vanilla MySQL and SQLite do not, and
  Postgres needs an extension or trigger pattern — verify the actual
  connector before recommending Tier 2.

## Do NOT

- Do NOT recommend event sourcing without an explicit architecture
  waiver from the user — Tier 3 is an architecture, not an audit
  mechanism.
- Do NOT ship any tier without its retention/growth answer — an
  unbounded audit table is an F7 defect by definition.
- Do NOT copy full row snapshots into audit records when a diff
  suffices — that is the denormalized-duplication failure (F4) applied
  to history.
