---
name: opp-closeout
description: >
  Close out a completed opportunity: pull its Connect invoices and open a Jira ticket to pay the
  LLO.
disable-model-invocation: false
---

# Opportunity Closeout

Process the financial closeout of a completed opportunity. Works on any
Connect opportunity: one ACE built in a run, or a live program's opportunity
named by its program context doc.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `opportunity_id` | the opportunity whose invoices are pulled | explicit arg; default: `runs/<run-id>/4-connect/connect-opp-setup.md`; Phase 9's partner opportunity is `phases.solicitation-management.products.selected_llo.opportunity_id` |
| `organization_slug` | org URL the invoice pages are read at | explicit arg; default: the run's holding org (`runConnectOrgs()`); else the program context doc |
| `llo_name`, `llo_org_slug` | who is paid (Jira summary, banking reference) | explicit arg; default: run_state `selected_llo`; else the program context doc |
| `run_id` | run-bound mode: closeout record path + decisions rows | optional; absent = live-program mode |
| `out_folder_id` | where the closeout record goes in live-program mode | explicit arg when `run_id` is absent |

**Live-program mode** (no `run_id`): Step 1 reads the opportunity live
(`connect_get_opportunity`, `connect_list_payment_units`) instead of the run
file; Step 4 writes the record to `out_folder_id` and logs it in the program
context doc's Decisions. The decisions-log rows below are run-only.

## Process

1. **Read opportunity details:**
   - Run mode: opportunity config from `ACE/<opp-name>/runs/<run-id>/4-connect/connect-opp-setup.md`
   - Live-program mode: `connect_get_opportunity({organization_slug, opportunity_id})`
     and `connect_list_payment_units`
   - Delivery/payment unit config

2. **Pull invoices** from Connect for this opportunity via
   `connect_list_invoices` (and `connect_get_invoice` for any that need
   detail hydration). Invoice atoms are conservative in 0.8.1 — they
   return empty/stub records for opps that haven't been billed yet.
   - Get auto-generated invoices based on verified deliveries
   - Calculate total payment amount
   - **If the invoice list is empty AND the opportunity has completed
     deliveries**, the invoice page shape may have evolved since
     0.8.1's probe — re-run `scripts/probe-connect-invoice.ts` to
     update the parser, or fall back to manual UI export until then.

3. **Create Jira ticket** for payment processing:
   - Project: appropriate Jira project for Connect payments
   - Summary: "Payment: [Opportunity Name] — [LLO Name]"
   - Description: invoice details, amount, LLO banking info reference
   - Attach invoice documents

4. **Write closeout record** to `ACE/<opp-name>/runs/<run-id>/10-closeout/opp-closeout_invoices.md`
   (live-program mode: `out_folder_id`):
   - Invoice details
   - Total amount
   - Jira ticket link

## MCP Tools Used
- Google Drive: `drive_read_file`, `drive_create_file`
- Connect (`ace-connect` MCP, 0.8.1+):
  - `connect_list_invoices` — pull invoices for the opportunity
  - `connect_get_invoice` — hydrate invoice detail
- Jira (Atlassian MCP): `createJiraIssue`

## Mode Behavior
- **Auto:** Pull invoices, create Jira ticket, proceed
- **Review:** Present invoice details for verification before creating ticket

## Dry-Run Behavior
When `--dry-run` is active:
- Write the Jira ticket specification (project, summary, description, attachments) and invoice details to `comms-log/dry-run-opp-closeout.md`
- Do not create the Jira ticket or pull invoices from Connect
- State tracks as `dry-run-success`

## Decisions Log

**Review fields (schema v6 — REQUIRED).** The decisions log is the run's review artifact (the build memo is retired). Every row this skill appends carries `plain` — one plain-language line for a programme partner who has never seen ACE — and, where the choice is visible somewhere a reviewer can open, `check_at` + `correct_looks_like`. The atom rejects a partner-facing row without `plain`, or with jargon in it. Rules, a worked row and the `review_ask` semantics: [`skills/_decisions-review-fields.md`](../_decisions-review-fields.md); field contract: `docs/decisions-contract.md`.

This skill writes load-bearing defaults to the per-run
`ACE/<opp-name>/runs/<run-id>/decisions.yaml`. The bar criterion and
schema live in `skills/idea-to-pdd/SKILL.md § Decisions Log Convention`
(canonical authority). The list below catalogs decisions that commonly
qualify under the bar for this phase — a working template, not a
required set. The skill applies the bar criterion and emits whatever
rows meet it; the catalog is a teaching device that improves over time.

### Common load-bearing decisions for Phase 10

| ID | Question | Map to surface |
|---|---|---|
| `closeout-depth` | Standard summary vs. deep retrospective with cycle-grade re-anchor? | `cycle-grade-eval` rubric input |
| `learnings-summary-scope` | Per-opp only, or cross-opp pattern aggregation? | `learnings-summary` skill output; ACE-wide pattern catalogue |

The orchestrator's Phase Write-Back Verifier (`agents/ace-orchestrator.md`
§ Phase Write-Back Contract § Decisions log clause) enforces the
contract; the renderer (`skills/decisions-render`) regenerates the gdoc
at end of every phase.

Each row this skill writes uses `phase: 10-closeout` and
`skill: opp-closeout`.


## Terminology

**The platform is `Connect`, never `CommCare Connect`** — in every word this skill
puts in front of a human. The full rule, including the carve-outs for CommCare the
mobile app, CommCare HQ and code-level identifiers, is
[`skills/_terminology.md`](../_terminology.md). Read it before writing prose; it is
binding on this skill's output.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-28 | Replace HITL workaround with `connect_list_invoices` + `connect_get_invoice` (ace-connect 0.8.1). Note: invoice page shape was not yet probed at 0.8.1 ship; atoms return conservative defaults until the page has been observed live | ACE team |
| 2026-10-18 | Add `## Inputs` as parameters (`opportunity_id`, `organization_slug`, LLO) with run defaults; live-program mode reads the opportunity live and records outside the run. ace#3148. | ACE (build-vs-maintain audit) |
| 2026-05-08 | Add `## Decisions Log` section: 2 anchor rows (closeout-depth, learnings-summary-scope) + bar-criterion reference. Pairs with decisions-log PR #4 (Phase 3-10 writes). | ACE team (decisions-log PR #4) |
