---
name: forge-docdrift
description: Detects drift between cited external docs (Claude Code, n8n nodes) and what our skills claim. Use before major n8n work or on /forge docs-check — doc drift, source verification, staleness.
---

# Forge playbook — Docdrift (external-doc claim drift detection)

**Do not duplicate existing tools — this is a NEW, narrow capability.** It does not replace `forge-scout`
(external-capability research/vetting) or `forge-audit-loop` (this project's own internal health) — it only
watches whether an external page a skill/doc CITES still backs up the claim made about it.

## Provenance (honesty)

This tool's IDEA came from researching `shanraisshan/claude-code-best-practice` (an external community
repo) — the Lead approved adopting the underlying idea ("keep external docs and our own claims about them in
sync") as one of 3 GH-research winners. **No code was copied.** `forge-bin/forge-docdrift.cjs` is a
Forge-native reimplementation built from scratch around this project's own conventions (zero-dep,
`config/orchestration/*.json` seed + `.claude/forge-research/*` state/ledger, `log-event.cjs`'s existing
`audit_finding` event type, the same injectable-fetcher hermetic-test seam every other network-touching
`forge-bin` tool uses). Provenance: **PATTERN_ADAPTED** (see the global research-recovery policy's honesty
vocabulary) — the pattern was adapted, not the implementation.

## What it does

`forge-bin/forge-docdrift.cjs check [--source <id>] [--json] [--run <run_id>]` reads
`config/orchestration/docdrift-sources.json` — a seeded list of REAL claims this project's own skills/docs
make that depend on an external, changeable page (an official Claude Code doc page, an n8n node doc page).
For each claim it fetches the real `source_url` (following redirects, timeout-bounded, zero-dependency
`node:https`/`node:http`) and searches the raw response body for every one of that claim's `check_tokens`.

Every claim is classified against its own persisted history in
`.claude/forge-research/docdrift-state.json`:
- **OK** — tokens found, claim was not drifted last known check.
- **NEW-DRIFT** — a token is missing, claim was NOT drifted before (first time this claim looks stale).
- **RECURRING** — a token is missing again, same as last known check (a standing, already-reported gap).
- **RESOLVED** — tokens found again after a prior drift (the doc caught back up, or the claim was fixed).
- **UNREACHABLE** — the fetch failed/timed out/returned non-2xx. **Never counts as drift** — the last KNOWN
  drift state is left exactly as it was. A network hiccup is not proof the docs changed.

Every check appends one line to `.claude/forge-research/docdrift-ledger.jsonl` (append-only, never
truncated) and persists the updated state. With `--run <run_id>`, ONE `audit_finding` event (already a
registered `log-event.cjs` event type — no new registration needed) is logged per **NEW-DRIFT** result only
— a RECURRING/RESOLVED/OK/UNREACHABLE result never re-fires an event for a condition already on record.

## Honest limits (read before trusting a result)

- **This is a heuristic token search, not a real diff against a known-good snapshot.** A missing token can
  mean the docs genuinely changed — or it can mean an unrelated redesign/paraphrase changed the wording while
  the underlying behavior is unchanged. Every report says **"possible drift, verify by hand"** — never "the
  docs changed" as an assertion of fact.
- **UNREACHABLE is not drift.** A network failure, timeout, or non-2xx response tells you nothing about
  whether the claim still holds — it is reported honestly as unreachable, and it never overwrites the
  claim's last known drift state.
- **Seeding a new claim requires reading BOTH files first**: the citing skill/doc (to state the claim
  accurately) AND the live source page (to pick `check_tokens` that are genuinely present right now). Never
  invent a claim or a token set without checking both.
- **Advisory only.** A DRIFT/RECURRING result never blocks a build, a doctor run, or a WP handoff — it is a
  signal for a human (or a future Boss) to go verify the cited doc by hand.

## When to use

- Before major n8n work (an n8n node's documented behavior — auth options, response mode — may have moved).
- Before relying on a cited Claude Code native feature (a subagent frontmatter field like `memory`/`hooks`/
  `isolation`, or a slash command like `/goal`/`/loop`) in a new skill or governance doc.
- On the owner's `/forge docs-check`.
- As one more check inside a periodic audit pass (alongside `forge-audit-loop`'s own MEMORY-INTEGRITY/
  AGENT-HEALTH/FEATURE-USAGE/DOCTOR-DELTA checks — this tool covers a gap none of those four checks touch:
  claims about content OUTSIDE this project).

## Adding a new claim

Edit `config/orchestration/docdrift-sources.json` — add `{id, skill, rule_id, category, check, check_tokens,
source_url, added}`. `id` must be unique; `check_tokens` must be a non-empty array of non-empty strings, each
independently searched (all must be present for the claim to read as OK); `source_url` must be `http(s)://`.
`forge-docdrift.cjs`'s own config loader (`loadSources()`) refuses a malformed entry outright (missing field,
empty `check_tokens`, non-http(s) URL, duplicate id) rather than silently skipping it.

## Skills / commands

`forge-bin/forge-docdrift.cjs` (`check` — the only command; `--source <id>` to check one claim, `--json` for
machine output, `--run <run_id>` to also log NEW-DRIFT findings as `audit_finding` events),
`config/orchestration/docdrift-sources.json` (the seeded claim list — the single source of truth for what is
checked), `.claude/forge-research/docdrift-state.json` (persisted drift memory, per-project, never a template
file), `.claude/forge-research/docdrift-ledger.jsonl` (append-only audit trail, per-project).

## Events

A real docdrift check with `--run <run_id>` logs `audit_finding` (the existing event type — never a new
registration) once per NEW-DRIFT claim, carrying the claim id, rule id, missing tokens, and source URL as
`evidence`. OK/RESOLVED/RECURRING/UNREACHABLE results are still recorded in the ledger but never generate a
duplicate event for a condition already on record.

## Fan-out & flow

**1 agent, no team.** Build Boss (or whichever Boss is doing the citing work) runs a docdrift check directly
— this is a single zero-dependency CLI call, not a multi-agent task.

## Ship-readiness (unique)

Every seeded claim's `check_tokens` were verified against the REAL live source page before being written to
`docdrift-sources.json` (never invented); a real check was actually run (not merely described) before any
report claims a verdict; every result names its literal status (OK/NEW-DRIFT/RECURRING/RESOLVED/UNREACHABLE)
— never blurred into a single "drift found: yes/no"; UNREACHABLE is reported as UNREACHABLE, never silently
treated as either OK or drift; nothing here ever blocks a build — it is advisory input for a human to verify.
