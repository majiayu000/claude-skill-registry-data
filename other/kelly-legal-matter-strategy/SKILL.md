---
name: kelly-legal-matter-strategy
description: Legal matter-strategy App-in-Skill (Busabase-backed) desk for new-case strategy, issue trees, evidence checklists, risk analysis, pleading outlines, and approval-gated drafting packs grounded in internal precedents. Use when the user invokes $kelly-legal-matter-strategy, mentions 案件策略, 办案辅助, 证据清单, 争议焦点, 文书生成辅助, litigation strategy, arbitration strategy, pleading outline, or wants a Busabase-backed desk where responsible lawyers review agent-prepared strategy before use.
metadata:
  category: legal
  tags:
    - risk:local-write
    - industry:legal
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-legal-matter-strategy
    resources:
      - items
      - entities
      - checks
      - settings
    risk: local-write

---

# Legal Matter Strategy

## Overview

Use this skill as a Busabase Cloud App-in-Skill desk. It builds reviewer-gated matter strategy packs from facts and internal precedents: issue tree, evidence map, risk posture, negotiation options, and pleading or memo outlines. Reading raw matter facts, deadlines, and evidence inventories is a genuine local-file operation a browser cannot perform: `scripts/create_strategy_batch.mjs` is the only place a strategy pack enters the system. The AirApp itself only reads Busabase and writes review decisions (approve / request changes / revise / block); `scripts/execute_decisions.mjs` records the planned follow-up, and `scripts/export_strategy_pack.mjs` is the only place an approved strategy pack leaves the system.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present stable refs such as `Strategy #1` and take verdicts in conversation.

## Business Role

Use this as the responsible-lawyer strategy gate for an active matter. It consumes client facts, deadlines, evidence inventories, and approved precedent packs, then produces issue trees, evidence maps, risk posture, negotiation options, and drafting outlines for review. Do not use it as a casebase ingestion tool, standalone legal research desk, or management analytics dashboard.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-legal-matter-strategy-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Legal Matter Strategy overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Legal Matter Strategy review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Matter-strategy command desk with partner review load, ready-to-draft strategies, blocked items, and activity.</td>
    <td><strong>Review queue</strong><br>Issue-tree and evidence-map recommendations with responsible-lawyer approval controls.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Legal Matter Strategy checks"></td>
    <td width="50%"><img src="assets/screenshots/workbench.webp" alt="Legal Matter Strategy workbench"></td>
  </tr>
  <tr>
    <td><strong>Checks</strong><br>Strategy QA for missing facts, evidence gaps, deadline caveats, precedent grounding, and risk warnings.</td>
    <td><strong>Workbench</strong><br>Detail pane for issue tree, evidence map, risk posture, negotiation options, and draft outline.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/entities.webp" alt="Legal Matter Strategy library"></td>
  </tr>
  <tr>
    <td><strong>Library</strong><br>Matter-strategy library of evidence and drafting plans, bucketed by review state.</td>
  </tr>
</table>

## Boundary

- The AirApp reads and writes Busabase records only. It never files documents, sends client advice, contacts counterparties, changes a case system, publishes brand claims, or performs any other external side effect.
- Ingesting a strategy batch is a local-file-only operation: `scripts/create_strategy_batch.mjs` reads a JSON payload file the agent prepares (from client facts, approved precedent packs, and evidence inventories) and writes it to Busabase. It never fetches or reads a source case-management system itself.
- Every legal position, client-facing output, external citation, filing step, or outbound message is approval-required and happens outside the app only after explicit human approval; `scripts/execute_decisions.mjs` never performs the export or downstream handoff itself — it only writes an execution marker.
- Treat legal work product, casebase data, client facts, personal data, trade secrets, and internal strategy as sensitive. Never commit local payload files, env files, or generated exports.

## Busabase Resources

Four Bases under one application Folder (`kelly-legal-matter-strategy`), declared in `content/kelly-legal-matter-strategy-app/app/js/config.js` and the generated template sidecars under `content/`:

- `items`: the matter-strategy workbench and review queue in one — issue tree, evidence map, risk posture, negotiation options, and pleading outline (matter stage, evidence gap count and list, negotiation options, posture, pleading outline, deadline), workflow status, and the human decision + execution marker on the same row.
- `entities`: matter families, issue clusters, or strategy lanes grouped by cause, stage, and responsible lawyer.
- `checks`: deterministic strategy QA checks for missing facts, evidence gaps, deadline caveats, precedent grounding, and unsupported legal positions, one row per check.
- `settings`: one row (`record-id: "config"`) with the firm profile, strategy policy (precedent-link/evidence-map/risk-scale/client-facing-approval rules), enabled drafting templates, and export preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/strategy-schema.md` for exact field shapes. Metrics and the recent-activity feed are recomputed client-side from the stored rows on every read (`content/kelly-legal-matter-strategy-app/app/js/matter-strategy-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/decision.

## First Run And Onboarding

On invocation, check the `items` Base. If it is empty, guide setup before ingesting real strategy packs: ask, turn by turn, enabled matter types and jurisdictions, strategy template preferences, evidence taxonomy and risk scale, and export destinations for approved strategy packs. Write the answers onto the Settings row, then ingest:

```bash
node skills/kelly-legal-matter-strategy/scripts/create_strategy_batch.mjs payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-legal-matter-strategy-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: strategy command desk with partner-review queue, evidence gaps, and deadline pressure.
- `#/review`: approval queue for strategy packs with issue trees, evidence notes, and risk posture.
- `#/items`: strategy workbench with editable plan, pleading outline, and negotiation options.
- `#/checks`: strategy QA checks for unsupported conclusions, evidence gaps, and approval-required legal positions.
- `#/entities`: matter library grouped by cause, stage, responsible lawyer, and outcome.
- `#/settings`: sanitized strategy template and provider configuration.

Demo mode:

- `?demo=1` or `?demo=overview` opens deterministic mock legal data for documentation and testing.
- `?demo=review`, `?demo=items`, `?demo=checks`, `?demo=entities`, and `?demo=detail` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language.
- Demo mode never reads or writes Busabase. Decision buttons still render but act on in-memory state only.

## Ingest Workflow

1. Clarify the client objective, procedural posture, deadline, jurisdiction, and available evidence before drafting strategy.
2. Ground every strategic recommendation in supplied facts, approved precedent packs, or explicit assumptions.
3. Run the write path:

```bash
node skills/kelly-legal-matter-strategy/scripts/create_strategy_batch.mjs payload.json --apply
```

The script validates required fields and upserts entities/items/checks into Busabase by natural id, so re-ingests are idempotent. Without `--apply` it is a dry run.

## Review Gates

- Block or request changes when the client objective, procedural posture, deadline, jurisdiction, evidence inventory, or assumptions are missing.
- Do not approve strategy that hides evidence gaps, relies on unapproved precedent, treats assumptions as facts, or phrases draft text as client advice before lawyer review.
- Export only approved or done packs with issue tree, evidence map, risk posture, options, deadline caveats, and use limits for downstream drafting.

## Decisions And Execution Workflow

1. The reviewer decides at `#/review` or the item workbench: approve, request changes (with a note), save an edited draft (revise), or block. Decisions write directly onto the item record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided item with the concrete operation — `export_strategy_pack` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the item's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `export_strategy_pack`, run `scripts/export_strategy_pack.mjs`; for `request_revision`, redraft the strategy per the review note and re-ingest.

## Export Workflow

1. `node skills/kelly-legal-matter-strategy/scripts/export_strategy_pack.mjs --out <dir>` reads items with a genuine human "approve" decision from Busabase and writes `approved-items.md`, `approved-items.json`, and `approved-items.csv` (default `exports/`, gitignored). Marks each exported item `status: "done"` in Busabase — this is the only write export performs, and it never happens for an item that merely has `status: "approved"` from a spoofed ingest payload without a real decision.
2. Filing, sending, settlement authority, and client advice happen only outside the app after explicit lawyer approval, through the user or a separate approved connector/skill.
3. Keep exports out of git and report the concrete file paths.

## Scripts

- `scripts/create_strategy_batch.mjs [--apply]`: parse a JSON payload and upsert entities/items/checks into Busabase.
- `scripts/execute_decisions.mjs [--apply]`: dry-run or apply a planned follow-up for approved/changes-requested items; never flips workflow status.
- `scripts/export_strategy_pack.mjs [--out <dir>]`: export genuinely approved items as Markdown, JSON, and CSV, and mark them done.

## Safety Defaults

- Do not fabricate facts, evidence, procedural deadlines, counsel approval, or expected judicial outcomes.
- Treat legal advice, settlement posture, filing strategy, and client communications as approval-required.
- If evidence is missing, mark the strategy as needing information rather than filling the gap.
- Approved exports are internal work product unless the responsible lawyer explicitly repurposes them elsewhere.

## Useful Commands

```bash
node skills/kelly-legal-matter-strategy/scripts/create_strategy_batch.mjs payload.json --apply
node skills/kelly-legal-matter-strategy/scripts/execute_decisions.mjs
node skills/kelly-legal-matter-strategy/scripts/execute_decisions.mjs --apply
node skills/kelly-legal-matter-strategy/scripts/export_strategy_pack.mjs --out exports/
pnpm --dir skills/kelly-legal-matter-strategy/content/kelly-legal-matter-strategy-app dev
```

In normal use, invoke `/kelly-legal-matter-strategy`, let the skill ingest what's due, and open the AirApp.
