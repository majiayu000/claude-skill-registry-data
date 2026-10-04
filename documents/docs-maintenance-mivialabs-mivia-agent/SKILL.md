---
name: docs-maintenance
description: Maintain the mivia-agent documentation. Trigger when the user asks to update, tidy, or restructure docs, when a code change needs docs updated, or when docs are out of date, wordy, or inconsistent.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - write_file
  - search_replace
---

# Docs maintenance

Keep the docs in this repo tidy, accurate, and current. Small change, big
rule: a doc that disagrees with the code is a bug as serious as the code
disagreeing with itself. Your job is to stop that drift.

## Read first

- `docs/README.md` — the index and the reading-order diagram. Every new or
  edited doc must stay in it.
- `docs/OWNERS.yaml` — maps each doc topic to one canonical path and one
  owner (product, architecture, quality, or security). One topic, one path.
  A second doc for an owned topic is drift.
- `docs/architecture/` — the design reference, split by concern: overview,
  concurrency, embedded-persistence, session-analysis, skills, workflows,
  workflow-stack-settle, token-usage-ledger. This repo has no single
  architecture.md and no ADRs; `docs/README.md` states ADRs are not used
  here.
- `AGENTS.md` — the writing standard (ASD-STE100) and the gate list. It is
  the contract. `CLAUDE.md` is a thin adapter that points back to it.

## The writing standard

ASD-STE100-style Simplified Technical English, per AGENTS.md and
`.agents/rules/90-writing-standard-ste100.md`.

- One idea per sentence. Instructional sentences stay at or below 20 words;
  descriptive sentences at or below 25.
- At most six sentences per paragraph.
- Nothing that is not true. Every claim must match the code. Check before
  you write it.
- No filler words: simply, just, seamless, robust, powerful, modern.
- Same thing, same word. No synonym drift.
- Prefer the present tense and the active voice.

## How to keep docs current

For any code change, ask: which doc covers this area, per `docs/OWNERS.yaml`?

When the user says "docs are out of date" without saying what changed, find
the delta first. Do not guess. Do this, in order:

1. Read `docs/OWNERS.yaml` and confirm the topic's canonical path.
2. Read the code the doc describes and confirm the doc's claims still
   match. A statement the code no longer supports is drift.
3. For provider docs specifically, cross-check the README provider table
   and `docs/architecture/overview.md` against
   `internal/provider/registry/registry.go` — `check_provider_docs.py`
   enforces this pairing.
4. `git diff` since the last doc commit to see what the code change was,
   then map it onto the right doc under `docs/architecture/`.

Only then edit.

After any edit, make `docs/README.md` reflect reality: update the index and
the reading-order diagram if a doc moved, was added, or was removed.

## The recorded API contract

`api/contracts/auth.v1.json` records the mivia API's `/v1/auth/*` surface:
routes, and the JSON field sets of the wire structs in
`internal/miviaauth`. It is hand-maintained, and
`internal/miviaauth/wire_contract_test.go` holds the Go code to it.

The API lives in `mivia-app-web` and checks in no OpenAPI document, so there
is nothing to generate from. Resync by reading the source files listed under
`source.paths` in the JSON, or by running the API locally:

```
curl -s http://localhost:3001/docs/json | python3 -m json.tool
```

This skill declares no command execution. Without it, read the source files
instead and report the resync as `NOT_RUN`.

Then update `source.transcribedOn`, per `api/contracts/README.md`. Never make
the test regenerate the JSON: the guarantee is that a person edits it.

## Watch the gates

- `make docs-check` runs `scripts/docs-check`, which confirms AGENTS.md,
  CLAUDE.md, `.agents/INDEX.md`, and the Copilot instructions file exist and
  cross-link, then runs `scripts/check_docs_ownership.py` (every
  `docs/**/*.md` has an owner in `docs/OWNERS.yaml`, every owned path
  exists, no duplicate H1 titles, no parallel doc for an owned topic) and
  `scripts/check_provider_docs.py`.
- `docs-check` is a prerequisite target inside `make verify`.
- After editing, `make verify` must exit 0. This skill declares no command
  execution: when the invoking agent has it, run the gate and report the
  exit status. Otherwise name the gate as `NOT_RUN` and say who must run
  it. Never report a gate as passing when nothing ran it.

## Scope discipline

- Docs only. Never change Go code, `.mivia/` config, or the gate scripts to
  make a doc pass. Change the doc.
- A new architecture doc goes under `docs/architecture/` with one owner in
  `docs/OWNERS.yaml`. Do not create a second doc for an already-owned topic.
- If a doc change is large (new architecture area, restructure, many
  files), route it through the delivery workflow: start it with
  `scripts/run-delivery-workflow.sh <label>` (see `AGENTS.md`, section
  "Workflow runs", and `.agents/skills/feature-delivery/SKILL.md`). Starting
  that run needs command execution this skill does not declare, so name it as
  the implementer's step.

## Done means verified

Report what you changed and the `make verify` result, or `NOT_RUN`
with the reason. If a gate failed, fix
the doc, not the gate. A green tree with truthful docs is the only "done".
