---
name: kelly-legal-precedent-desk
description: Legal precedent App-in-Skill (Busabase-backed) desk for internal casebase search, local court-pattern analysis, similar-case packs, citations, and approval-gated research exports. Use when the user invokes $kelly-legal-precedent-desk, mentions 类案检索, 本地裁判尺度, 内部案例库查询, 案例查阅与收藏, precedent research, similar cases, legal research pack, or wants a Busabase-backed desk where lawyers review agent-prepared precedent findings before reuse.
metadata:
  category: legal
  tags:
    - risk:local-write
    - industry:legal
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-legal-precedent-desk
    resources:
      - items
      - entities
      - checks
      - settings
    risk: local-write

---

# Legal Precedent Desk

## Overview

Use this skill as a Busabase Cloud App-in-Skill desk. It finds and packages internal precedents for a new legal question: similar facts, local court tendencies, decisive evidence, holdings, citations, and a reviewer-approved research memo. Searching the approved internal casebase and preparing a research pack is a genuine local-file operation a browser cannot perform: `scripts/create_research_batch.mjs` is the only place a research pack enters the system. The AirApp itself only reads Busabase and writes review decisions (approve / request changes / revise / block); `scripts/execute_decisions.mjs` records the planned follow-up, and `scripts/export_research_pack.mjs` is the only place an approved research pack leaves the system.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present stable refs such as `Pack #1` and take verdicts in conversation.

## Business Role

Use this as the research gate between the approved internal casebase and matter work. It turns a focused legal question into reviewed similar-case packs with match rationale, local court pattern notes, citations, and use limits. Do not use it to ingest raw documents, decide case strategy by itself, or publish external citations without lawyer approval.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-legal-precedent-desk-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Legal Precedent Desk overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Legal Precedent Desk review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Precedent command desk with packs awaiting review, high-match cases, approved packs, and recent activity.</td>
    <td><strong>Review queue</strong><br>Similar-case packs with local court-pattern notes, citations, evidence, and approval controls.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Legal Precedent Desk checks"></td>
    <td width="50%"><img src="assets/screenshots/workbench.webp" alt="Legal Precedent Desk workbench"></td>
  </tr>
  <tr>
    <td><strong>Checks</strong><br>Quality checks for citation traceability, similarity rationale, jurisdiction fit, and confidentiality limits.</td>
    <td><strong>Workbench</strong><br>Detail view for precedent reasoning, decisive facts, internal citations, draft memo, and review note.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/entities.webp" alt="Legal Precedent Desk library"></td>
  </tr>
  <tr>
    <td><strong>Library</strong><br>Internal precedent and trial-court pattern library, bucketed by review state.</td>
  </tr>
</table>

## Boundary

- The AirApp reads and writes Busabase records only. It never files documents, sends client advice, contacts counterparties, changes a case system, publishes brand claims, or performs any other external side effect.
- Ingesting a research batch is a local-file-only operation: `scripts/create_research_batch.mjs` reads a JSON payload file the agent prepares (from the approved internal casebase and new matter facts) and writes it to Busabase. It never fetches or reads a source case-management system itself.
- Every legal position, client-facing output, external citation, filing step, or outbound message is approval-required and happens outside the app only after explicit human approval; `scripts/execute_decisions.mjs` never performs the export or downstream handoff itself — it only writes an execution marker.
- Treat legal work product, casebase data, client facts, personal data, trade secrets, and internal strategy as sensitive. Never commit local payload files, env files, or generated exports.

## Busabase Resources

Four Bases under one application Folder (`kelly-legal-precedent-desk`), declared in `content/kelly-legal-precedent-desk-app/app/js/config.js` and the generated template sidecars under `content/`:

- `items`: the precedent research workbench and review queue in one — matched similar cases, similarity scores, local court-pattern notes, citations (research question, jurisdiction, match count and high-match count, top/average similarity, court pattern, citation count), workflow status, and the human decision + execution marker on the same row.
- `entities`: issue clusters, court-pattern groups, or precedent collections grouped by issue, court, outcome, and lawyer.
- `checks`: deterministic precedent QA checks for citation traceability, similarity rationale, jurisdiction fit, and confidentiality limits, one row per check.
- `settings`: one row (`record-id: "config"`) with the firm profile, search policy (default jurisdiction, minimum similarity score, require source case ids, quote limit words), and export preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/precedent-schema.md` for exact field shapes. Metrics and the recent-activity feed are recomputed client-side from the stored rows on every read (`content/kelly-legal-precedent-desk-app/app/js/precedent-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/decision.

## First Run And Onboarding

On invocation, check the `items` Base. If it is empty, guide setup before ingesting real research packs: ask, turn by turn, enabled jurisdictions and practice areas, similarity fields and citation policy, quote and confidentiality limits, and research-pack export preferences. Write the answers onto the Settings row, then ingest:

```bash
node skills/kelly-legal-precedent-desk/scripts/create_research_batch.mjs payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-legal-precedent-desk-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: precedent research desk with open questions, match quality, and local court-pattern summaries.
- `#/review`: approval queue for precedent packs with citations, quote snippets, and reviewer notes.
- `#/items`: research-pack workbench with question, answer outline, similar cases, and recommended use.
- `#/checks`: citation and confidentiality checks for source coverage, quote limits, and internal-use labels.
- `#/entities`: similar-case library grouped by issue, court, outcome, and lawyer.
- `#/settings`: sanitized casebase/search-policy configuration.

Demo mode:

- `?demo=1` or `?demo=overview` opens deterministic mock legal data for documentation and testing.
- `?demo=review`, `?demo=items`, `?demo=checks`, `?demo=entities`, and `?demo=detail` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language.
- Demo mode never reads or writes Busabase. Decision buttons still render but act on in-memory state only.

## Ingest Workflow

1. Clarify the new matter facts, legal question, target jurisdiction, and whether the output is for internal research, client advice, or drafting support.
2. Search the approved internal casebase and prepare a precedent pack with similarity rationale, court-pattern notes, citations, and use limits.
3. Run the write path:

```bash
node skills/kelly-legal-precedent-desk/scripts/create_research_batch.mjs payload.json --apply
```

The script validates required fields and upserts entities/items/checks into Busabase by natural id, so re-ingests are idempotent. Without `--apply` it is a dry run.

## Review Gates

- Block or request changes when similar-case support is too thin, citation traceability is missing, jurisdiction or court level does not fit, confidentiality labels are absent, or the pack overstates an outcome.
- Approve only when each finding has a similarity rationale, source-backed citations, local court-pattern caveats, and a clear internal-use or external-use limit.
- Export only approved or done packs. Matter strategy may consume approved packs; client advice, filings, and public citations require separate lawyer approval outside this app.

## Decisions And Execution Workflow

1. The reviewer decides at `#/review` or the item workbench: approve, request changes (with a note), save an edited draft (revise), or block. Decisions write directly onto the item record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided item with the concrete operation — `export_research_pack` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the item's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `export_research_pack`, run `scripts/export_research_pack.mjs`; for `request_revision`, strengthen the research pack per the review note and re-ingest.

## Export Workflow

1. `node skills/kelly-legal-precedent-desk/scripts/export_research_pack.mjs --out <dir>` reads items with a genuine human "approve" decision from Busabase and writes `approved-items.md`, `approved-items.json`, and `approved-items.csv` (default `exports/`, gitignored). Marks each exported item `status: "done"` in Busabase — this is the only write export performs, and it never happens for an item that merely has `status: "approved"` from a spoofed ingest payload without a real decision.
2. Client advice, filings, settlement authority, and public citation happen only outside the app after explicit lawyer approval, through the user or a separate approved connector/skill.
3. Keep exports out of git and report the concrete file paths.

## Scripts

- `scripts/create_research_batch.mjs [--apply]`: parse a JSON payload and upsert entities/items/checks into Busabase.
- `scripts/execute_decisions.mjs [--apply]`: dry-run or apply a planned follow-up for approved/changes-requested items; never flips workflow status.
- `scripts/export_research_pack.mjs [--out <dir>]`: export genuinely approved items as Markdown, JSON, and CSV, and mark them done.

## Safety Defaults

- Do not present internal precedent findings as final legal advice or guaranteed outcomes.
- Keep client names and privileged strategy out of exported packs unless expressly approved.
- Every quoted snippet must trace to an approved case record and respect the configured quote policy.
- If the internal casebase does not contain enough similar cases, say so and route to external legal research instead of inventing support.

## Useful Commands

```bash
node skills/kelly-legal-precedent-desk/scripts/create_research_batch.mjs payload.json --apply
node skills/kelly-legal-precedent-desk/scripts/execute_decisions.mjs
node skills/kelly-legal-precedent-desk/scripts/execute_decisions.mjs --apply
node skills/kelly-legal-precedent-desk/scripts/export_research_pack.mjs --out exports/
pnpm --dir skills/kelly-legal-precedent-desk/content/kelly-legal-precedent-desk-app dev
```

In normal use, invoke `/kelly-legal-precedent-desk`, let the skill ingest what's due, and open the AirApp.
