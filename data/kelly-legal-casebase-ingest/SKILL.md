---
name: kelly-legal-casebase-ingest
description: Legal casebase App-in-Skill (Busabase-backed) intake and anonymization QA desk for law-firm judgment and award documents. Use when the user invokes $kelly-legal-casebase-ingest, mentions internal case database, 智能案例库, 裁判文书入库, 脱敏, 结构化, 分类标注, 案例审核, 质量验收, or wants a Busabase-backed desk where reviewers approve, revise, or block agent-prepared case records before they become searchable knowledge assets.
metadata:
  category: legal
  tags:
    - risk:local-write
    - industry:legal
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-legal-casebase-ingest
    resources:
      - items
      - entities
      - checks
      - settings
    risk: local-write

---

# Legal Casebase Ingest

## Overview

Use this skill as a Busabase Cloud App-in-Skill desk. It turns archived judgments and arbitral awards into reviewed internal case records: anonymization checks, issue tags, court/cause metadata, reasoning snippets, and reviewer approval before ingest. Reading a judgment/award document is a genuine external operation a browser cannot perform: `scripts/ingest_documents.mjs` is the only place a case record enters the system. The AirApp itself only reads Busabase and writes review decisions (approve / request changes / revise / block); `scripts/execute_decisions.mjs` records the planned follow-up, and `scripts/export_case_records.mjs` is the only place an approved record leaves the system as a searchable knowledge asset.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present stable refs such as `Intake #1` and take verdicts in conversation.

## Business Role

Use this as the upstream quality gate for the legal knowledge system. It converts source documents into anonymized, source-backed case records that can feed precedent research and firm analytics after approval. Do not use it to answer a new legal question, build matter strategy, or prepare management conclusions; route those to the downstream legal skills after the case record is approved.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-legal-casebase-ingest-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Legal Casebase Ingest overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Legal Casebase Ingest review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Casebase command desk with intake progress, anonymization risk, review load, and recent activity.</td>
    <td><strong>Review queue</strong><br>Approval-gated case records with stable refs, anonymization evidence, review notes, and decision controls.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Legal Casebase Ingest checks"></td>
    <td width="50%"><img src="assets/screenshots/workbench.webp" alt="Legal Casebase Ingest workbench"></td>
  </tr>
  <tr>
    <td><strong>Checks</strong><br>Deterministic QA checks for PII leakage, taxonomy completeness, source coverage, and tag confidence.</td>
    <td><strong>Workbench</strong><br>Detail pane for facts, reasoning, legal basis, tags, editable draft, and reviewer note before ingest.</td>
  </tr>
</table>

## Boundary

- The AirApp reads and writes Busabase records only. It never files documents, sends client advice, contacts counterparties, changes a case system, publishes brand claims, or performs any other external side effect.
- Ingesting a document is a local-file-only operation: `scripts/ingest_documents.mjs` reads a JSON payload file the agent prepares (from anonymized facts, structuring, and tagging) and writes it to Busabase. It never fetches or reads a source document itself.
- Every legal position, client-facing output, management report, external citation, filing step, or outbound message is approval-required and happens outside the app only after explicit human approval; `scripts/execute_decisions.mjs` never performs the export or downstream handoff itself — it only writes an execution marker.
- Treat legal work product, casebase data, client facts, personal data, trade secrets, and internal strategy as sensitive. Never commit local payload files, env files, or generated exports.

## Busabase Resources

Four Bases under one application Folder (`kelly-legal-casebase-ingest`), declared in `content/kelly-legal-casebase-ingest-app/app/js/config.js` and the generated template sidecars under `content/`:

- `items`: the case-record workbench and review queue in one — anonymization/taxonomy facts (cause, court, procedure, outcome, source paragraphs, extraction confidence, duplicate score, redaction flags), workflow status, and the human decision + execution marker on the same row.
- `entities`: the canonical case-library groupings by cause, court, lawyer, and status — not raw source documents.
- `checks`: deterministic QA checks for PII leakage, missing metadata, source coverage, and tag confidence, one row per check.
- `settings`: one row (`record-id: "config"`) with the firm profile, ingestion/anonymization/taxonomy policy, and export preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/casebase-schema.md` for exact field shapes. Metrics and the recent-activity feed are recomputed client-side from the stored rows on every read (`content/kelly-legal-casebase-ingest-app/app/js/casebase-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/decision.

## First Run And Onboarding

On invocation, check the `items` Base. If it is empty, guide setup before ingesting real documents: ask, turn by turn, case-source folders or handoff export format, allowed document types and jurisdictions, anonymization policy and reviewer sampling rate, and required taxonomy fields (cause, court, procedure, lawyer, outcome). Write the answers onto the Settings row, then ingest:

```bash
node skills/kelly-legal-casebase-ingest/scripts/ingest_documents.mjs payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-legal-casebase-ingest-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: intake command desk with ingest progress, QA burden, anonymization risk, and recent activity (derived from each item's own timestamps).
- `#/review`: approval queue for case records with anonymization evidence and reviewer notes.
- `#/items`: case-record workbench with facts, court reasoning, legal basis, tags, and source snippets.
- `#/checks`: deterministic QA checks for PII leakage, missing metadata, source coverage, and tag confidence.
- `#/entities`: canonical case library preview grouped by cause, court, lawyer, and status.
- `#/settings`: sanitized config summary, onboarding state, and data-provider status.

Demo mode:

- `?demo=1` or `?demo=overview` opens deterministic mock legal data for documentation and testing.
- `?demo=review`, `?demo=items`, `?demo=checks`, `?demo=entities`, and `?demo=detail` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language.
- Demo mode never reads or writes Busabase. Decision buttons still render but act on in-memory state only.

## Ingest Workflow

1. Collect document exports from the matter system or a safe local folder; never paste full privileged files into chat when paths can be used.
2. Run the agent extraction pass to produce records with facts, issues, holdings, legal basis, tags, and anonymization evidence.
3. Run the write path:

```bash
node skills/kelly-legal-casebase-ingest/scripts/ingest_documents.mjs payload.json --apply
```

The script validates required fields and upserts entities/items/checks into Busabase by natural id, so re-ingests are idempotent. Without `--apply` it is a dry run.

## Review Gates

- Block or request changes when PII evidence is missing, anonymization checks fail, duplicate risk is unresolved, required taxonomy is incomplete, source coverage is thin, or extraction confidence is low.
- Approve only when the record has enough facts, reasoning, legal basis, tags, and source pointers for downstream reuse without exposing raw client names or privileged source text.
- Export only genuinely approved records (a real `decideItem` "approve" decision, not a spoofed ingest payload), and keep downstream visibility explicit: precedent desk and firm radar may consume sanitized records; client advice and filings remain outside this app.

## Decisions And Execution Workflow

1. The reviewer decides at `#/review` or the item workbench: approve, request changes (with a note), save an edited draft (revise), or block. Decisions write directly onto the item record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided item with the concrete operation — `export_case_record` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the item's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `export_case_record`, run `scripts/export_case_records.mjs`; for `request_revision`, redraft the record per the review note and re-ingest.

## Export Workflow

1. `node skills/kelly-legal-casebase-ingest/scripts/export_case_records.mjs --out <dir>` reads items with a genuine human "approve" decision from Busabase and writes `approved-items.md`, `approved-items.json`, and `approved-items.csv` (default `exports/`, gitignored). Marks each exported item `status: "done"` in Busabase — this is the only write export performs, and it never happens for an item that merely has `status: "approved"` from a spoofed ingest payload without a real decision.
2. Downstream consumption (precedent desk, firm radar) happens only outside the app after explicit approval, through the user or a separate approved connector/skill.
3. Keep exports out of git and report the concrete file paths.

## Scripts

- `scripts/ingest_documents.mjs [--apply]`: parse a JSON payload and upsert entities/items/checks into Busabase.
- `scripts/execute_decisions.mjs [--apply]`: dry-run or apply a planned follow-up for approved/changes-requested items; never flips workflow status.
- `scripts/export_case_records.mjs [--out <dir>]`: export genuinely approved items as Markdown, JSON, and CSV, and mark them done.

## Safety Defaults

- Treat all source documents, parties, trade secrets, personal data, and attorney work product as sensitive.
- Do not ingest a record if anonymization evidence is missing, PII-risk checks fail, or reviewer approval is absent.
- Preserve enough facts, reasoning, and legal application for reuse while minimizing raw source text.
- Never expose private source text, secrets, or real client names through demo data, screenshots, logs, or config summaries.
- Use stable ids and natural-key upserts so repeated ingests, executions, and exports are idempotent.

## Useful Commands

```bash
node skills/kelly-legal-casebase-ingest/scripts/ingest_documents.mjs payload.json --apply
node skills/kelly-legal-casebase-ingest/scripts/execute_decisions.mjs
node skills/kelly-legal-casebase-ingest/scripts/execute_decisions.mjs --apply
node skills/kelly-legal-casebase-ingest/scripts/export_case_records.mjs --out exports/
pnpm --dir skills/kelly-legal-casebase-ingest/content/kelly-legal-casebase-ingest-app dev
```

In normal use, invoke `/kelly-legal-casebase-ingest`, let the skill ingest what's due, and open the AirApp.
