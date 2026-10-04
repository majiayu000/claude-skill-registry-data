---
name: kelly-legal-firm-radar
description: Legal-firm radar App-in-Skill (Busabase-backed) dashboard for anonymized casebase analytics, practice-area mix, case-quality indicators, lawyer capability profiles, brand proof points, and approval-gated management reports. Use when the user invokes $kelly-legal-firm-radar, mentions 律师画像, 律所经营分析, 业务布局分析, 案件质量评估, 专业人才梯队, 律师全息品牌, casebase analytics, law-firm management dashboard, or wants a Busabase-backed desk where partners review agent-prepared management insights before export.
metadata:
  category: legal
  tags:
    - risk:local-write
    - industry:legal
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-legal-firm-radar
    resources:
      - items
      - entities
      - checks
      - settings
    risk: local-write

---

# Legal Firm Radar

## Overview

Use this skill as a Busabase Cloud App-in-Skill desk. It uses anonymized internal casebase metadata to prepare management insights: practice mix, local court outcomes, lawyer capability profiles, quality indicators, and approved brand or staffing reports. Reading raw casebase/practice-area/lawyer metrics is a genuine local-file operation a browser cannot perform: `scripts/import_metrics.mjs` is the only place a metric or insight enters the system. The AirApp itself only reads Busabase and writes review decisions (approve / request changes / revise / block); `scripts/execute_decisions.mjs` records the planned follow-up, and `scripts/export_management_report.mjs` is the only place an approved management report leaves the system.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, import what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present stable refs such as `Insight #1` and take verdicts in conversation.

## Business Role

Use this as the partner review gate for firm-level analytics. It consumes anonymized casebase metadata and approved summaries to prepare practice mix, lawyer capability, quality, staffing, and brand proof insights with methodology notes. Do not use it for matter strategy, legal advice, raw document review, compensation decisions, or external marketing claims without separate approval.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-legal-firm-radar-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Legal Firm Radar overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Legal Firm Radar review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Firm radar command desk with partner review load, approved reports, blocked insights, and management activity.</td>
    <td><strong>Review queue</strong><br>Approval-gated management insights for practice mix, lawyer profiles, and brand proof points.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Legal Firm Radar checks"></td>
    <td width="50%"><img src="assets/screenshots/workbench.webp" alt="Legal Firm Radar workbench"></td>
  </tr>
  <tr>
    <td><strong>Checks</strong><br>Analytics QA for anonymization, sample size, attribution, bias caveats, and external-use restrictions.</td>
    <td><strong>Workbench</strong><br>Detail pane for practice analytics, talent signals, quality indicators, and approved management report text.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/entities.webp" alt="Legal Firm Radar library"></td>
  </tr>
  <tr>
    <td><strong>Library</strong><br>Practice-area and lawyer capability profile cards, grouped by review state.</td>
  </tr>
</table>

## Boundary

- The AirApp reads and writes Busabase records only. It never files documents, sends client advice, contacts counterparties, changes a case system, publishes brand claims, or performs any other external side effect.
- Importing metrics is a local-file-only operation: `scripts/import_metrics.mjs` reads a JSON payload file the agent prepares (from anonymized casebase/practice-area/lawyer metrics) and writes it to Busabase. It never fetches or reads a source casebase system itself.
- Every legal position, client-facing output, management report, external citation, filing step, or outbound message is approval-required and happens outside the app only after explicit human approval; `scripts/execute_decisions.mjs` never performs the export or downstream handoff itself — it only writes an execution marker.
- Treat legal work product, casebase data, client facts, personal data, trade secrets, and internal strategy as sensitive. Never commit local payload files, env files, or generated exports.

## Busabase Resources

Four Bases under one application Folder (`kelly-legal-firm-radar`), declared in `content/kelly-legal-firm-radar-app/app/js/config.js` and the generated template sidecars under `content/`:

- `items`: the management-insight workbench and review queue in one — practice mix/quality/talent/brand-proof analytics facts (sample size, reporting period, visibility, lawyer count, public-citable count, quality indicators), workflow status, and the human decision + execution marker on the same row.
- `entities`: practice-area groupings and lawyer capability profile cards derived from anonymized casebase metadata — not raw case documents.
- `checks`: deterministic analytics QA checks for anonymization, sample size, attribution, and unsupported claims, one row per check.
- `settings`: one row (`record-id: "config"`) with the firm profile, analytics policy (anonymization/sample-size/external-brand-claim rules), practice taxonomy, optional outcome-trend series, and export preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/firm-radar-schema.md` for exact field shapes. Metrics and the recent-activity feed are recomputed client-side from the stored rows on every read (`content/kelly-legal-firm-radar-app/app/js/firm-radar-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last import/decision.

## First Run And Onboarding

On invocation, check the `items` Base. If it is empty, guide setup before importing real metrics: ask, turn by turn, casebase metadata source, practice taxonomy and lawyer roster fields, allowed metrics for internal management versus external brand use, and management report export preferences. Write the answers onto the Settings row, then import:

```bash
node skills/kelly-legal-firm-radar/scripts/import_metrics.mjs payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-legal-firm-radar-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: firm analytics desk with practice mix, outcome trends, talent signals, and review queue.
- `#/review`: approval queue for management insights, brand proof points, and staffing recommendations.
- `#/items`: insight workbench with methodology, evidence, suggested action, and visibility limits.
- `#/checks`: analytics QA checks for sample size, privacy, attribution, and unsupported claims.
- `#/entities`: lawyer and practice-area profile cards from anonymized metadata.
- `#/settings`: sanitized taxonomy, provider, and onboarding state.

Demo mode:

- `?demo=1` or `?demo=overview` opens deterministic mock legal data for documentation and testing.
- `?demo=review`, `?demo=items`, `?demo=checks`, `?demo=entities`, and `?demo=detail` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language.
- Demo mode never reads or writes Busabase. Decision buttons still render but act on in-memory state only.

## Import Workflow

1. Collect anonymized metadata only: case type, court, outcome, lawyer/team, dates, and approved tags. Do not import raw confidential documents for management analytics.
2. Prepare insight cards for business layout, quality review, talent planning, or brand proof points with methodology and caveats.
3. Run the write path:

```bash
node skills/kelly-legal-firm-radar/scripts/import_metrics.mjs payload.json --apply
```

The script validates required fields and upserts entities/items/checks into Busabase by natural id, so re-imports are idempotent. Without `--apply` it is a dry run.

## Review Gates

- Block or request changes when sample size is too small, anonymization is weak, methodology is unclear, lawyer attribution is unfair, or an external brand claim lacks public-citable proof.
- Approve only when the report states period, sample size, taxonomy, caveats, visibility, and whether each proof point is internal-only or public-citable.
- Export only genuinely approved reports (a real `decideItem` "approve" decision, not a spoofed import payload). Keep internal management reports separate from external brand material unless partners explicitly approve the external use.

## Decisions And Execution Workflow

1. The reviewer decides at `#/review` or the item workbench: approve, request changes (with a note), save an edited draft (revise), or block. Decisions write directly onto the item record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided item with the concrete operation — `export_management_report` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the item's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `export_management_report`, run `scripts/export_management_report.mjs`; for `request_revision`, redraft the insight per the review note and re-import.

## Export Workflow

1. `node skills/kelly-legal-firm-radar/scripts/export_management_report.mjs --out <dir>` reads items with a genuine human "approve" decision from Busabase and writes `approved-items.md`, `approved-items.json`, and `approved-items.csv` (default `exports/`, gitignored). Marks each exported item `status: "done"` in Busabase — this is the only write export performs, and it never happens for an item that merely has `status: "approved"` from a spoofed import payload without a real decision.
2. External brand use happens only outside the app after explicit partner approval, through the user or a separate approved connector/skill.
3. Keep exports out of git and report the concrete file paths.

## Scripts

- `scripts/import_metrics.mjs [--apply]`: parse a JSON payload and upsert entities/items/checks into Busabase.
- `scripts/execute_decisions.mjs [--apply]`: dry-run or apply a planned follow-up for approved/changes-requested items; never flips workflow status.
- `scripts/export_management_report.mjs [--out <dir>]`: export genuinely approved items as Markdown, JSON, and CSV, and mark them done.

## Safety Defaults

- Do not rank lawyers or publish brand claims from small samples without caveats and partner approval.
- Use anonymized metadata for analytics; keep client names, raw documents, private financials, and privileged notes out of the dashboard.
- Treat talent, compensation, hiring, and external marketing claims as approval-required.
- If metrics are incomplete or biased, mark the insight as needing more data rather than overstating conclusions.

## Useful Commands

```bash
node skills/kelly-legal-firm-radar/scripts/import_metrics.mjs payload.json --apply
node skills/kelly-legal-firm-radar/scripts/execute_decisions.mjs
node skills/kelly-legal-firm-radar/scripts/execute_decisions.mjs --apply
node skills/kelly-legal-firm-radar/scripts/export_management_report.mjs --out exports/
pnpm --dir skills/kelly-legal-firm-radar/content/kelly-legal-firm-radar-app dev
```

In normal use, invoke `/kelly-legal-firm-radar`, let the skill import what's due, and open the AirApp.
