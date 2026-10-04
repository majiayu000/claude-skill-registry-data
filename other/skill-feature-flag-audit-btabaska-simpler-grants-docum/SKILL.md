---
name: Feature Flag Audit
description: Inventory every feature flag in the monorepo, classify it (release gate, kill switch, experiment, permission), report its state per environment, age, and readiness for removal. Triggers on 'flag audit', 'feature flag inventory', 'list flags'. Produces a Markdown table plus a shortlist of removal candidates.
---

## Purpose

Keep the feature-flag surface honest. The skill inventories all flags, groups them by purpose, and highlights flags that are fully rolled out or fully dark so they can be scheduled for cleanup. Complements the `flag-cleanup` skill, which executes the removal.

## When to Invoke

- Monthly or pre-release flag hygiene pass.
- Before running `flag-cleanup` on any single flag.
- When ops wants a current-state report of the flag surface.

## When NOT to Invoke

- Mid-incident (flag toggles are in flight; the audit will lie).
- For UI-only A/B experiments tracked outside the flag system.

## Inputs

- **scope** (optional): `api`, `frontend`, `infra`, or `all` (default).
- **environments**: list, default `dev,staging,prod`.

## Procedure

1. Collect flag names from:
   - `infra/` SSM parameter definitions.
   - `api/src/` usages of the feature-flag service.
   - `frontend/src/hooks/useFeatureFlag` callers.
2. Cross-reference the SSM values per environment (from Terraform state or the SSM API if available; otherwise from the `.tfvars`).
3. Classify each flag:
   - `release-gate` — gates a new feature.
   - `kill-switch` — disables a feature during incidents.
   - `experiment` — A/B or percentage rollout.
   - `permission` — access control.
4. Compute age from the earliest `git log` touch of the flag identifier.
5. Mark removal candidates:
   - Release gate ON in all envs for > 60 days.
   - Kill switch never toggled for > 180 days.
6. Emit the table plus candidate shortlist.

## Outputs

```
Feature Flag Audit

Flag                         Type          Dev   Stg   Prod  Age    Candidate
feature_new_search           release-gate  on    on    on    92d    YES
kill_application_submit      kill-switch   off   off   off   210d   YES
experiment_results_layout_b  experiment    50%   50%   10%   30d    no
perm_agency_admin            permission    on    on    on    420d   no (permission)
```

## Safety

- Read-only. Never toggles flags.
- Never flags a `permission`-class flag for removal.
- Flags sourced from code only; environment values are reported as best-known, with a staleness warning if Terraform state is older than 24 hours.
- FedRAMP: prod flag values are never written to logs or PR bodies by default; include `environments=prod` explicitly to opt in.

## Examples

**Example 1 — Monthly hygiene.** Shortlist of 5 removal candidates; dev schedules `flag-cleanup` for each.

**Example 2 — Pre-release sweep.** Confirms no release-gate is accidentally off in staging before cutover.

**Example 3 — Scoped audit.** `scope=frontend` lists only frontend-consumed flags.

## Related

- `.cursor/skills/flag-cleanup/` — removes a fully-rolled-out flag.
- `.cursor/agents/feature-flag.md` — adds new flags.
