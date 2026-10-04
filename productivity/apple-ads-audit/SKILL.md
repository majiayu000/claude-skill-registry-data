---
name: apple-ads-audit
description: 'Use for read-only diagnostics of a connected Apple Ads account: account health, live campaign and ad-group structure, traffic ownership, duplicate exact keywords, missing cross-negatives, serving problems, spend without results, or a simple same-window comparison of Apple total installs and Adapty installs. Triggers on "audit my Apple Ads account", "what is broken", "which campaigns need attention", "is my live structure correct", or "why are Apple and Adapty installs different". Never use it to design a new account, run a weekly review, or make changes.'
license: MIT
---

# Audit a live Apple Ads account

Read the account, explain what is observable, and stop before any mutation. This skill has no write
path. Route proposed fixes to `apple-ads` only after the user chooses an action.

When the full plugin is installed, use the operating skill's synced CLI references for command
syntax:

- `../apple-ads/references/asa-management.md` for entity and catalog reads.
- `../apple-ads/references/asa-metrics.md` for performance reads and metric definitions.

When this skill was installed alone and those files are absent, use
`adapty asa <topic> <command> --help` for the installed version. The playbooks name the allowed
read commands. Never reconstruct a missing flag or endpoint from memory.

## Preflight

Run `adapty asa whoami` first in every session.

- If the CLI, authentication, subscription, or Apple connection is unavailable, hand off to
  `adapty-cli-setup` and stop.
- If access is ready, resolve the organization, app, and requested scope from list results. Never
  invent or reuse an identifier from a different company.
- If the user has no connected account and wants a proposed structure, use `apple-ads-strategy`.

## Route one audit question

Open `references/INDEX.md` and read the one playbook it names.

- Overall health, serving, performance warnings, or Apple-versus-Adapty installs →
  `references/playbooks/account-health.md`.
- Live structure, duplicate targets, traffic ownership, or missing cross-negatives →
  `references/playbooks/structure-audit.md`.
- A weekly or monthly operating review → `apple-ads`, then its `weekly-review.md` playbook.

Do not run both audit playbooks by default. Finish the requested audit, then offer the other as a
separate follow-up if the evidence points there.

## Read-only boundary

Allowed work:

- `whoami`, `list`, `get`, `metrics`, and `metrics overview` reads.
- Normalizing and comparing returned entities.
- Producing findings and a proposed handoff.

Forbidden work:

- Any `create`, `update`, `add`, `sync`, pause, enable, or automation mutation.
- Including a ready-to-run write command in the audit result.
- Asking for approval to write while this skill is active.

When the user asks to fix a finding, close the audit and hand the chosen finding to `apple-ads` as a
new task. The operator must re-resolve ids and obtain its own confirmation.

## Diagnostic method

1. **Frame the question.** Record the app, scope, date window, success metric, and any user-defined
   limit. Ask only for missing inputs that materially affect the result.
2. **Plan the reads.** Use list counts for entity counts and server aggregation for metrics. Keep
   the standard audit inside the analytics budget; never loop per entity or per day.
3. **Normalize evidence.** Give each returned row or metadata fact an evidence id. Keep the source,
   window, entity id, and metric attached to it; include a cohort window only for `revenue`, `roas`,
   `arpu`, `arppu`, `arpas`, or `roi`.
4. **Separate layers.** Write the observation first, then the explanation, then the recommendation.
   Never present an explanation as observed fact.
5. **Apply applicability.** Mark controls that cannot be evaluated as `unknown` or
   `not_applicable`; do not score them as failures.
6. **Report and stop.** Recommend the smallest useful next action, but do not execute it.

## Finding contract

Every audit response contains:

1. `summary` — a short plain-language answer.
2. `scope` — company, app, entity scope, and identifiers used.
3. `date_window` — exact dates and grouping, plus a cohort window only for a cohort root.
4. `findings` — ordered by severity.
5. `evidence` — ids that map every claim to returned data.
6. `confidence` — overall confidence and the limiting missing data.
7. `unknowns` — questions the available surface cannot settle.
8. `recommended_actions` — read-only follow-ups or operator handoffs.

Each finding contains:

| Field | Meaning |
|---|---|
| `status` | `healthy`, `attention`, `critical`, `unknown`, or `not_applicable` |
| `observation` | What the returned data directly shows |
| `explanation` | The simplest supported interpretation, clearly labeled |
| `evidence` | Evidence ids, metric names, windows, and affected entity ids |
| `confidence` | `high`, `medium`, or `low`, with a reason |
| `recommendation` | The next read or an `apple-ads` handoff |
| `limitations` | What prevents a stronger conclusion |

Use `critical` only for a confirmed serving failure or a user-defined limit that was actually
breached. Use `attention` for a supported concern without that proof. Never invent a numeric health
score or universal threshold.

## Simple install comparison

This is the entire attribution scope of this skill:

- Compare `total_installs` from Apple with `adapty_installs` from Adapty for the same scope and exact
  date window.
- Show both values and `absolute_gap = apple_installs - adapty_installs`.
- Show `relative_gap = absolute_gap / apple_installs` only when `apple_installs > 0`.
- If either value is absent, mark the comparison `unknown`. If Apple installs are zero, say the
  percentage is undefined.
- Explain plainly that the systems use different attribution and event definitions, so an exact
  match is not expected.
- Do not diagnose attribution, assign fault, or claim a cause.

## Evidence and confidence

- **High:** direct metadata or a server-aggregated metric for the exact scope and window.
- **Medium:** multiple direct signals support the interpretation, but the CLI does not expose the
  cause or change history.
- **Low:** the conclusion depends on names, inferred intent, a thin sample, missing value data, or
  mismatched maturity.

Name correlation as correlation: use "coincided with" when change history is unavailable, never
"was caused by".

## Failure modes

- A missing business target means report facts, not winners and losers.
- A thin or immature cohort means `unknown`, not unprofitable.
- An unscoped metadata read can mix apps or campaigns; stop and resolve scope.
- A `429` that reaches the agent means stop. Do not sleep and retry in a loop.
- A request to redesign a future account belongs to `apple-ads-strategy`.
- A request to change anything belongs to `apple-ads` after the audit is complete.
