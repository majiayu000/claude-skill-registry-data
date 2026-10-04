---
name: monitor
description: Conviction-trigger surveillance via Quartr keyword alerts — parse every active thesis's Conviction Triggers for named observables, propose keyword alerts scoped to the Vault Active watchlist (or market-wide for macro observables), create them ONLY on explicit user confirmation, and reconcile the alert set against the book as theses open/close. Use when user says "monitor", "set up alerts", "keyword alerts", "watch for X", or "reconcile alerts".
model: opus
effort: medium
allowed-tools: Read Grep Glob Edit Write ToolSearch mcp__quartr Bash(date * jq * ls * cat * grep * printf * wc *)
---

Operationalises [G-13]: every thesis names the datapoint that would confirm or kill it first — this skill puts a standing tripwire on that datapoint in the primary-source stream. Alerts live in the Quartr app (that is where they fire — there is NO vault-side push); the loop is: alert fires in Quartr → user inspects → `/transcript TICKER --event <id>` or `/ingest` the hit → normal vault propagation. This skill's job is keeping the alert set faithful to the book: proposing alerts from trigger language, creating them only with consent, and pruning them when theses close.

**Account-state discipline (the skill's defining constraint):** `create_keyword` / `update_keyword` / `delete_keyword` mutate the user's Quartr account — Tier-3-adjacent territory. Every mutation is proposed in a table and executed only after **explicit user confirmation in an interactive session**. In a non-interactive/headless run, mutations are NEVER executed: the proposal table goes into the report and the run ends there. No exceptions, including "obviously good" alerts.

## Arguments

- `/monitor` — full reconcile: parse triggers, diff against live alerts, propose creates + deletes
- `/monitor --list` — read-only: current alerts vs current trigger set, with provenance
- `/monitor --prune` — deletions only (closed/downgraded theses, retired triggers)
- `/monitor "<term>" TICKER` — single ad-hoc proposal (e.g. a `/sweep` finding worth a standing alert)

## Step 0: Pre-flight

1. **Lock**: `vault-wide` per `_shared/preflight.md` Procedure 1, timeout 5 min (writes only `.data/quartr_keywords.json`; reads theses).
2. **Quartr probe** (hard): per `_shared/quartr.md` §1 load `list_keywords,create_keyword,update_keyword,delete_keyword,list_watchlists`. Unavailable → abort.
3. **State**: read `.data/quartr_watchlist.json` (watchlistId — alerts scope to it) and `.data/quartr_keywords.json` (the provenance registry, schema below; absent → empty). Watchlist state missing → abort with `run /event-sweep --setup first` (market-wide-only alerts without a watchlist scope are a noise machine).
4. **Mental models**: skipped — mechanical extraction + scoping judgement, no investment conclusions (load-tiering).

Registry schema (`.data/quartr_keywords.json`) — the vault-side memory of WHY each alert exists:

```json
{"<quartr keyword id>": {"name": "<term>", "ticker": "TICKER", "trigger": "<the →HIGH/LOW/CLOSE clause it watches, first ~80 chars>",
  "scope": "watchlist|all", "documentTypes": ["transcript","report"], "created": "YYYY-MM-DD"}}
```

## Step 1: Extract observables from Conviction Triggers

Per active thesis, read `## Conviction Triggers` (targeted section read). From each `→ HIGH/LOW/CLOSE if` clause, extract candidate keywords that satisfy ALL of:

- **Specific**: a named product, technology, program, metric name, customer relationship, or coined term (`CoWoS allocation`, `MLPerf Training`, `Tomahawk Ultra`, `capacity auction`, `18A Clearwater Forest`) — never generic vocabulary (`revenue`, `margin`, `guidance`, `competition`, `China`) whose alert would fire on half the corpus.
- **3-40 characters** (API constraint) — compress or split longer observables; drop what cannot be compressed without losing specificity.
- **Utterable**: something a management or analyst would actually SAY on the record. A numeric threshold (`capex below $20B`) is not utterable — extract its subject (`capex`) only if paired with a specific object, else skip and note the trigger as `not alertable — numeric threshold, /numbers territory`.

Cap the proposal set at **15 per run** (alert fatigue destroys the channel); prioritise `conviction: high` theses, then triggers with no existing alert, then LOW/CLOSE triggers over HIGH (downside tripwires earn priority — losses cost more to recover, [G-9]).

## Step 2: Scope each candidate

- **Default `watchlist`** (`companySetting: "watchlists"`, `watchlistIds: [Vault Active]`): the observable matters when any book name discusses it — including the cross-company case (a supplier saying `CoWoS allocation` matters for AMD; the watchlist scope catches it because both are members).
- **`all` (market-wide)** only for observables whose signal source is structurally OUTSIDE the book (macro/regulatory terms, an uncovered competitor's product name). Flag these in the proposal table — market-wide alerts are the noisy tier and each must justify itself.
- `documentTypes`: default `["transcript", "report"]` (spoken + filed; slides add noise). Note in the proposal when a candidate warrants slides too (product-launch terms).

## Step 3: Reconcile

Diff candidates against `list_keywords` + the registry:
- Candidate with no live alert → **propose CREATE**.
- Live alert whose registry ticker is no longer `status: active`, or whose trigger clause no longer exists in the thesis (trigger retired/rewritten) → **propose DELETE** (this is `--prune`'s whole job).
- Live alert with no registry entry (created by hand in the app) → list as `unmanaged — adopt into registry? (no mutation proposed)`.
- Name/scope drift (e.g. thesis renamed the observable) → propose UPDATE.

## Step 4: The confirmation gate

Present one table: `# · action · term · scope · docTypes · ticker · trigger it watches (verbatim clause fragment)`. Ask the user to confirm by numbers/ranges/`all` — creates and deletes confirmed separately (deleting surveillance is as consequential as adding it). Only then execute the confirmed mutations, one call per item; write every executed mutation into the registry (creates add entries keyed by the returned keyword id; deletes remove them). Partial confirmation is normal — unconfirmed rows are dropped silently, not queued.

Non-interactive session → print the table under `## Proposed (NOT executed — non-interactive run)` and stop.

## Step 5: Release lock + report

Alert census (live count, managed vs unmanaged, coverage: how many active theses have ≥1 alert), mutations executed this run, the not-alertable triggers list (these need `/numbers`/`/catalyst`-style numeric watching instead — say so), and the reminder that fires land in the Quartr app: check it, then `/transcript --event` the hit.

## Design constraints (xxx DO NOT VIOLATE xxx)

1. **No mutation without explicit interactive confirmation.** The proposal table IS the deliverable; execution is the optional second act. Headless runs never mutate.
2. **The registry is the contract.** An alert without provenance (which thesis, which trigger) cannot be reconciled and becomes permanent noise — every skill-created alert gets a registry entry atomically with creation.
3. **Specificity bar over coverage.** Ten sharp alerts beat forty vague ones; the generic-vocabulary ban is absolute. A trigger that yields no utterable specific keyword is reported as not-alertable, not force-fitted.
4. **This skill never touches theses.** Trigger text is read-only input; rewriting a trigger to make it alertable is `/deepen`'s decision with the user, not this skill's.
5. **Watchlist scope is read-only.** Membership belongs to `/event-sweep` (contract §3 of that skill); `/monitor` scopes alerts to the watchlist but never edits it.
