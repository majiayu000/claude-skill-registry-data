---
name: kelly-legal-contracts
description: Legal-contract review desk (Busabase App-in-Skill) for NDAs, MSAs, DPAs, and SOWs. Use when the user invokes $kelly-legal-contracts or /kelly-legal-contracts, mentions legal, 法务, contract review, 合同审阅, NDA, MSA, DPA, SOW, redlines, clause playbook, legal intake, issue list, or wants a Busabase-backed review desk where a human legal reviewer approves, revises, or blocks agent-prepared contract issues.
metadata:
  category: legal
  tags:
    - risk:gated-write
    - industry:legal
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-legal-contracts
    resources:
      - contracts
      - issues
      - checks
      - claims
      - claim-rules
      - settings
    risk: gated-write

---

# Kelly Legal Contracts

## Overview

Use this skill as the legal-contract review desk. The agent ingests contract facts and extracted clauses, drafts clause issues (risk notes, fallback language, negotiation notes) against a company clause playbook, runs deterministic risk checks, and gives the reviewer a Busabase-backed App-in-Skill review queue (approve / request changes / block) plus an approval-gated issue-list export. Reading a contract document or a legal intake is a genuine external operation a browser cannot perform: `scripts/ingest_contracts.mjs` is the only place a contract or issue enters the system, `scripts/run_checks.mjs` runs the risk-check rules, and `scripts/execute_decisions.mjs` records the planned follow-up for approved/changes-requested issues. The AirApp itself only reads Busabase and writes review decisions; export happens through `scripts/export_issues.mjs`, and every outbound legal position, redline, counterparty message, signature, or filing is delegated to the user or a separate approved connector after explicit approval.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest/check what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; then present numbered issues (`Issue #1`) and take verdicts in conversation.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Legal Contracts overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Kelly Legal Contracts review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Legal command desk with contract × workstream status, risk pass rate, review queue preview, and recent activity.</td>
    <td><strong>Review queue</strong><br>Approval-gated legal issue queue with approve / request changes / block decisions and audit notes.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Kelly Legal Contracts risk checks"></td>
    <td width="50%"><img src="assets/screenshots/issues.webp" alt="Kelly Legal Contracts issue workbench"></td>
  </tr>
  <tr>
    <td><strong>Risk checks</strong><br>Per-rule pass/warn/fail results across clause issues, including hard-stop terms and playbook violations.</td>
    <td><strong>Clause issues</strong><br>Editable issue detail with fallback language, memo fields, reviewer rationale, and risk-check evidence.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-legal-contracts-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- This skill assists legal operations and contract review; it does not provide final legal advice and does not replace licensed counsel or an authorized legal reviewer.
- Ingesting a contract or issue is a local-file-only operation: `scripts/ingest_contracts.mjs` reads a JSON payload file the agent prepares (from contract text, summaries, or a legal intake) and writes it to Busabase. It never fetches documents from remote systems on its own.
- The AirApp reads and writes Busabase records only. It never sends redlines, emails counterparties, accepts terms, signs contracts, deletes files, or performs any other external side effect.
- Every outbound legal position, redline, counterparty message, approval, signature, filing, or waiver is approval-required and happens outside the app only after explicit human approval; `scripts/execute_decisions.mjs` never performs the send itself — it only writes an execution marker.
- If a hard-stop term is present (`uncapped liability`, `perpetual data retention`, broad indemnity, missing DPA terms), block or request changes rather than weakening the rule.
- Treat contracts, counterparties, and playbooks as sensitive. Never commit local payload files, env files, or generated exports. Never expose raw secrets or private playbooks through logs, reports, screenshots, or demo data.

## Busabase Resources

Six Bases under one application Folder (`kelly-legal-contracts`), declared in `content/kelly-legal-contracts-app/app/js/config.js` and the generated template sidecars under `content/`:

- `contracts`: the contract library — counterparty, matter type, governing-law/deal facts, key obligations, watch terms, and the required-document checklist.
- `issues`: the clause-issue workbench and review queue in one — workstream-specific fields (risk notes, fallback language, negotiation notes, memo, business ask, structured facts), workflow status, risk score, and the human decision + execution marker on the same row.
- `checks`: per-issue, per-rule risk-check results (required fields, title length, hard-stop terms, restricted positions, risk-note/business-ask counts, memo length, all-caps noise, watch-term repetition, document checklist, clause-playbook violations).
- `claims`: the clause playbook's approved fallback clauses and rejected positions.
- `claim-rules`: the clause playbook's hard-stop / restricted-phrase rules.
- `settings`: one row (`record-id: "config"`) with the legal profile, per-workstream rule sets, hard-stop/restricted terms, and export preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/contracts-schema.md` for exact field shapes. Risk scores, the review queue, the recent-activity feed, and metrics are recomputed client-side from the stored rows on every read (`content/kelly-legal-contracts-app/app/js/contracts-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/checks run.

## First Run And Onboarding

On invocation, check the `issues` Base. If it is empty, guide setup before ingesting real contracts: ask, turn by turn, legal profile (company/entity, reviewer role, preferred risk scale), enabled workstreams (`nda`, `msa`, `dpa`, `sow`) with per-workstream rule sets, jurisdictions, hard-stop terms, escalation policy, and export preferences. Write the answers onto the Settings row, then ingest and check:

```bash
node skills/kelly-legal-contracts/scripts/ingest_contracts.mjs payload.json --apply
node skills/kelly-legal-contracts/scripts/run_checks.mjs --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-legal-contracts-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: legal command desk — KPI cards (contracts, issues, risk pass rate, exported this week), contract × workstream status matrix, review-queue preview, recent activity (derived from each issue's own timestamps).
- `#/contracts` and `#/contracts/<contract_id>`: the contract library — counterparty, matter type, source badge, workstreams, linked issues. Detail shows contract facts, key obligations, watch terms, the required-document checklist, and linked issues.
- `#/issues` and `#/issues/<issue_id>`: the clause-issue workbench — counterparty, workstream, jurisdiction, title, risk score, workflow status. Detail shows an editable field workbench (title, risk notes, fallback language, negotiation notes, memo, business ask, or structured facts depending on the workstream), reviewer rationale, and per-rule risk-check evidence.
- `#/checks`: risk-check results — every rule per issue with pass/warn/fail badges and evidence, filterable by rule, workstream, contract, and result.
- `#/claims`: the clause playbook — approved fallback clauses, rejected positions, and hard-stop/restricted-phrase rules.
- `#/review`: the review queue — every issue with its workflow state (`needs_review` / `changes_requested` / `approved` / `done` / `blocked`), risk summary, agent suggestions, `Review note`, decision buttons (approve / request changes / block), and a stable ref (`Issue #1`). Decisions write directly onto the issue record through `busabase-sdk`; field edits saved in the workbench arrive as `revise` decisions carrying the edited fields.
- `#/settings`: sanitized config summary — legal profile, per-workstream rule sets, hard-stop/restricted-term counts, export prefs, read live off the Settings Base.

Demo mode:

- `?demo=overview`, `?demo=contracts`, `?demo=issues`, `?demo=checks`, `?demo=claims`, `?demo=review`, and `?demo=detail` open deterministic mock scenes for documentation and screenshots.
- `lang=en` or `lang=zh` forces UI chrome language; contract/legal terms may stay in English when that is realistic.
- Deep links such as `/?demo=review&lang=zh#/review` must work.
- Demo mode never reads or writes Busabase. Decision buttons still work in the UI but act on in-memory state only.

UI language: English and Chinese chrome with `Auto` default. Keep real contract content, counterparty names, and legal positions in their original language.

## Ingest Workflow

1. Collect inputs: contract type, counterparty, our entity, governing law, deal owner, target date, business ask, extracted clause text, and company playbook positions.
2. Draft the issue as a structured ingest payload per the workstream's field shape (`nda`: title/risk-notes/fallback-language/negotiation-notes/redline-outline; `msa`: title/fallback-language/memo; `dpa`: title/business-ask; `sow`: title/subtitle/fallback-language/structured-facts). Include the contract facts if the contract does not exist yet.
3. Run the write path:

```bash
node skills/kelly-legal-contracts/scripts/ingest_contracts.mjs payload.json --apply
```

The script validates the payload against the workstream field shapes and the required-fields rules stored on the Settings row, normalizes contracts/issues, and upserts them into Busabase by natural key (`contract_id`/name+counterparty, `issue_id`) so re-ingests are idempotent. Without `--apply` it is a dry run.

## Check Workflow

1. Run `node skills/kelly-legal-contracts/scripts/run_checks.mjs --apply`. Deterministic rules (required fields, title length, hard-stop terms, restricted positions, risk-note/business-ask counts, memo length, all-caps noise, watch-term repetition, document checklist, clause-playbook violations) are computed from the workstream rule sets on the Settings row and the clause playbook (`claims`/`claim-rules` Bases); per-issue risk scores are recomputed idempotently.
2. Summarize failures for the reviewer by ingesting `compliance_summary`/`suggestions` onto the issue record.
3. Give the user the AirApp URL and send them to `#/review`.

## Decisions And Execution Workflow

1. The reviewer decides at `#/review` or the issue workbench: approve, request changes (with a note), save edited fields (revise), or block. Decisions write directly onto the issue record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided issue with the concrete operation — `export_issue_list` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the issue's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `export_issue_list`, run `scripts/export_issues.mjs` and hand off the redline/counsel communication through the user or a separate approved connector after approval; for `request_revision`, redraft the issue per the review note, re-ingest, and re-run checks.

## Export Workflow

1. `node skills/kelly-legal-contracts/scripts/export_issues.mjs --out <dir>` reads issues with a genuine human "approve" decision from Busabase and writes each as a clean Markdown issue memo plus `issues.csv` (default `exports/`, gitignored). Marks each exported issue `done` in Busabase — this is the only write export performs, and it never happens for an issue that merely has `status: "approved"` from a spoofed ingest payload without a real decision.
2. Actual sending, redline generation, counterparty communications, CLM updates, signature, or filing happen only outside the app after explicit approval, through the user or a separate approved connector/skill.
3. Keep exports out of git and report the concrete file paths.

## Safety Defaults

- Never fabricate legal approval, waiver, signature authority, regulatory conclusion, or attorney review.
- Treat legal, privacy, money, IP, employment, and dispute-related terms as approval-required.
- Do not send issue lists, redlines, fallback clauses, or counterparty messages without an explicit `approve` decision.
- Use stable ids and natural-key upserts so repeated ingests, checks, and executions are idempotent.
- If the issue payload and the workstream rule set disagree (unknown fields), stop and reconcile before executing.

## Useful Commands

```bash
node skills/kelly-legal-contracts/scripts/ingest_contracts.mjs payload.json --apply
node skills/kelly-legal-contracts/scripts/run_checks.mjs --apply
node skills/kelly-legal-contracts/scripts/execute_decisions.mjs
node skills/kelly-legal-contracts/scripts/execute_decisions.mjs --apply
node skills/kelly-legal-contracts/scripts/export_issues.mjs --out exports/
pnpm --dir skills/kelly-legal-contracts/content/kelly-legal-contracts-app dev
```

In normal use, invoke `/kelly-legal-contracts`, let the skill ingest/check what's due, and open the AirApp.
