---
name: orphex-meta-delivery-audience-review
description: "Review Meta ad-set delivery, audience context, reporting status, and mature outcome trends to identify supported constraints and bounded tests."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Meta Delivery & Audience Review

Review the actual Meta campaign/ad-set delivery context and business outcome. Interpret platform status as a diagnostic signal, not a causal explanation or a reason to change the optimization goal automatically.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at levels `adgroup` and `audience` for dated delivery and outcomes, and `insights.read` for Meta; delivery status and learning phase are live platform reads. If `playbook.catalog` lists the frequency-capping or placement efficiency playbook, run it with `playbook.run`.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Align evidence

Record account timezone, currency, objective, performance goal, optimization event, attribution setting/date basis, conversion maturity, entity scope, budget owner, actual status/reason, schedule, audience controls/exclusions, placement settings, and material edits. Keep lead, landing-view, link-click, and purchase outcomes distinct. Verify current account/API field definitions and availability before comparing exports; names and supported controls can differ by campaign type.

Calculate outcome CPA, link CTR, CPM, and within-scope frequency only when their exact inputs are supplied. Reach and unique audience measures are nonadditive across ad sets, days, or overlapping audiences. Do not sum reach, average frequency, or infer audience overlap from repeated targeting descriptions. Observed frequency has no universal fatigue threshold and cannot prove saturation or self-competition.

## Rank delivery explanations

Separate eligibility/policy or instrumentation problems, supplied learning diagnostics, budget/pacing, bid/cost controls, audience availability, placement mix, creative age/edits, and conversion-path evidence. Do not invent a fixed event-volume requirement or assert that every edit resets learning. Status, event counts, and coincident edits alone do not identify the reason; use the actual diagnostic and current official account documentation. A recent incomplete conversion window can explain apparent deterioration but requires demonstrated lag.

Distinguish optimization suggestions/signals from hard audience constraints for the actual setup. Do not recommend broad expansion, blanket exclusions, switching to an easier goal, or overlapping clone campaigns without a business reason and valid supported controls. Prefer one bounded test tied to the diagnosed constraint with a mature review window and a guardrail.

Deliver observations, supported constraints, unresolved hypotheses, next diagnostic/test, and change scope. Preserve purchase/lead-quality goals and keep all account edits within explicit authorization.

## Official references

- [Meta Marketing API Insights fields and reporting](https://developers.facebook.com/docs/marketing-api/insights/)
- [Meta learning-phase help; availability may require sign-in](https://www.facebook.com/business/help/112167992830700)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.
