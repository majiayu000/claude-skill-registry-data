---
name: project-context
description: Use when a project's durable context needs to be seeded or refreshed — creating or updating docs/product/context.md (overview + digest + source index + glossary + Know/Don't-Know ledger + design context + technical context) in the target repo; when a project has no context layer yet (Stage-0 setup); when domain terminology is still forming or has drifted; after a meeting, new evidence batch, or scope change that outdates the current context. Also use to ingest new docs/product/input/ batches into the digest. Do not use for repo scaffolding or CI setup, for writing the discovery plan, PRD, or epics (use discovery-plan, prd-writer, epics), or for creating or revising Jobs to be Done — this skill records finished JTBDs by id and marks missing ones TBD; jobs-to-be-done owns minting them.
metadata:
  version: 0.2.0
  owner: Alvaro Bezerra
  provenance: ported 2026-07-24 from product-craft project-context (github.com/ABZerra/product-craft) and adapted to the A-Team contract — two files (glossary.md + project-overview.md) merged into the canonical docs/product/context.md.
---

# project-context

Seed or refresh the project's **durable context layer**: a single
`docs/product/context.md` holding the overview, the digest of raw evidence, the
source index, the glossary, the design and technical context sections, and the
Know/Don't-Know ledger. This file is what every other A-Team
skill — and every agent in the pipeline — reads instead of holding project facts.
The canonical shape is `references/context-template.md` (mirrored in
`CONTRACT.md`).

This skill is **pure craft**: zero project facts live in it. It is the entry
door those facts walk through.

**Glossary first, always.** Domain language stabilizes in the glossary before it
stabilizes anywhere else — seed it on day one even if only three terms are
known. A settled vocabulary is what keeps every downstream artifact (jobs, PRDs,
briefs, tickets) speaking the same language.

## Where it writes

**Repo-first-and-always.** Resolve the target root in this order:

1. A **git repo** — from an explicit target path argument, else the CWD's git
   root. If a repo is satisfied, use it and move on.
2. A **Cowork / plain project folder** — valid when no repo exists or the user
   explicitly targets one. Never a blocker.

Either way the write path is the same: `<target>/docs/product/context.md`, with
raw evidence under `<target>/docs/product/input/`. Git-commit the change only
where a repo exists — one commit per run, message naming what changed and why
(e.g. `docs(context): ingest 2026-07-24 client call; 3 glossary terms settled`).

## Current authority index and selective reads

Resolve the target's existing `current context` config binding before choosing a
write path; it overrides the default path above. Maintain one fenced
`ateam-context` JSON index in that document using `runner/CONTEXT.md`. Keep purpose,
audience, observed state, authority order, global invariants, design/engineering
bindings, commands, unresolved decisions and authoritative source links concise.
Record exact source hashes; facts distinguish accepted intent from observation.

For every non-bootstrap task run
`node <harness>/runner/src/context-cli.mjs select --root <target> --task '<task JSON>'`.
Pass paths, linked obligations and behavior/risk tags. Stop on stale/conflicting
context or an exceeded configured budget. Revalidate relevant sources; do not
import every archive or infer changed intent from built code. If no index exists,
bootstrap it from reviewed existing authority and explicit unknowns, preserve the
narrative/history, then rerun selection before starting downstream phases.

After verified integration, use the `refresh` command documented in
`runner/CONTEXT.md` with the integration receipt and affected observed facts.
This preserves prior facts/provenance. Product intent changes use the existing
human decision path; a completion refresh cannot authorize them.

## When to use

- A project has no context layer yet (Stage-0 setup) — seed `context.md` from
  whatever the human has: docs, links, a conversation.
- New evidence landed in `docs/product/input/` and needs digesting.
- Terminology has shifted, scope or framing changed, or a meeting changed
  direction — the context is stale.
- Someone new (human or agent) needs "read this one file" to get productive.

## When NOT to use

- Repo structure, stack selection, CI setup — out of scope entirely.
- Writing the discovery plan, PRD, or epics — this skill feeds those; route to
  `discovery-plan`, `prd-writer`, `epics`.
- Defining or revising the project's jobs — that belongs to `jobs-to-be-done`.
  This skill cites finished JTBDs **by id, quoting headline language exactly**,
  and writes `Core job: TBD` when none exists. It never mints or rewrites jobs.

## Inputs

- Which target (ask if ambiguous — never guess between projects).
- Any existing `docs/product/context.md` — a refresh preserves what's still
  true and updates only what changed. **Never rebuild from scratch over an
  existing file.**
- `docs/product/input/` batches not yet listed in the file's `ingested:`
  frontmatter — these are the ingestion queue.
- Whatever the user tells you directly.
- **Anything the human points at outside the repo — stage first.** A file in
  a parent folder, an attachment in the conversation, a board, a shared page:
  copy it verbatim as `input/<YYYY-MM-DD>-<label>/` with a `SOURCE.md`
  (origin · authoring date if stated · what was copied and what was not · any
  fidelity caveat — an extraction is not the document) **before** citing it.
  A document that names a companion not in hand: record the absence in
  `SOURCE.md` and as a ledger entry; never infer its contents. Prior human
  work on the same question (a board, a current-state map) is staged the same
  way — a FigJam board via `get_figjam` as
  `input/<YYYY-MM-DD>-figjam-<board>-pulled/` — the returned JSON verbatim as
  `board.json` plus a generated `board.md` node listing, named as a rendering
  in `SOURCE.md`.
- **Connectors (pull, then stage).** If Notion, Granola, Slack, or the ops API
  are available and hold relevant context, you may pull — but every pull is
  first saved **verbatim** as a new clearly-labeled batch,
  `input/<YYYY-MM-DD>-<source>-pulled/`, and then digested from there like any
  human-dropped evidence. Never edit, delete, or summarize-in-place an existing
  batch; digests belong in `context.md`. Never block on a connector or ask the
  user to connect one.

## Workflow

1. **Resolve the target** (repo-first, above). Read the current `context.md`
   and its `ingested:` list; read `docs/product/jtbd/` ids if present.
2. **Gather.** Collect un-ingested `input/` batches, user input, and staged
   connector pulls. Don't pad thin input into fake completeness — a short honest
   file beats a long speculative one.
3. **Glossary first.** Capture every domain term in play: settled terms with
   working definitions, forming terms with the best current definition,
   uncertain terms explicitly TBD. When two names compete for one concept,
   record both and note which is winning. Never delete a renamed term — note
   the rename so old documents stay readable.
4. **Digest.** Per new batch: compress what the evidence actually says, each
   claim cited to a line (`<batch>/<file>:L<start>-L<end>`, `§<n>`, or
   `:p<N>` for a PDF). **Read every prose file in full.** A long one —
   300 lines or more — goes to a one-shot digest subagent — announce it,
   pass the file path and the current glossary, expect back a digest whose
   every claim cites lines plus the terms and conflicts it found — so
   coverage is `full · <date> · digest` rather than the conductor skimming.
   The digest is written knowing how Design and
   Dev will later consume it — organised, not just summarized. **Conflicts
   are items:** where this batch disagrees with another batch, the glossary,
   a Know, an active job, an active ADR or the shipped state, write a
   `[conflict]` ledger entry with both citations (step 7); never smooth it.
   On an iteration run, end the batch's digest with the job classification —
   kept / reshaped / superseded, trigger cited — that `jobs-to-be-done`'s
   iteration step produced.
5. **Sources.** Index everything this refresh consumed — links visited,
   human-provided files, connector pulls, the grill digest batch: type ·
   pointer (URL or `input/` path) · date · what it informed · **coverage**
   (`full · <date> · conductor` · `full · <date> · digest` · `partial
   <range> · <date> · <method>`, the last for non-prose only).
   Every evidence file in every ingested batch gets a row (the batch's own
   `SOURCE.md` none); prose files are `full`; a row that predates the column
   carries `legacy · <original date>`, and a legacy file you re-read gets a
   fresh row. Every row resolves; Overview's Key links stay the 2–3
   load-bearing ones.
6. **Overview.** What/why in one paragraph, audience, stage, goals,
   constraints, key links. Jobs cited by id, headline quoted exactly.
7. **Ledger.** Update Know / Don't-Know. Tag each Don't-Know **blocking**
   (naming the JTBD or scope call it blocks) or **non-blocking** (destined for
   `research-plan.md` as an open question). Enter each conflict from step 4 as
   a **`[conflict]`** entry — both sides cited, what it blocks, and its ruling
   if a batch's `SOURCE.md` precedence settles it — a conflict between files of
   that batch only — (`ruling: SOURCE.md precedence — <which>`); otherwise
   `ruling: open`, for the grill. Knows cite lines; an inherited Know
   without one is tagged `[legacy]`, never back-filled. Uncertainty stays
   visible as TBD — a confident-sounding guess is a landmine for every
   skill that reads this file.
8. **Design and technical context.** On a first run, synthesize the design
   briefing's answers (from the `intake/` design bank) into `## Design
   context` — users & emotional goals, brand personality, aesthetic direction
   with references and anti-references, accessibility, 3–5 design principles —
   and the dev bank's answers into `## Technical context` — stack binding,
   external dependencies, infra/deploy, data sensitivity, non-functional
   constraints, v0 test bar. On a refresh, preserve both sections and update only what the
   human changed; dropping either is a forbidden overwrite like any other
   section.
   **Settled facts only, in both.** An uncertain or assumed fact belongs in
   `research-plan.md` with a confidence level, a machine-readable one in the
   target's `## A-Team Config`. One fact, one home — never restate across
   files, because both copies are durable and will eventually disagree.
9. **Read-back — mandatory before writing.** `context.md` is a durable
   artifact: present the drafted file (or the diff, on a refresh) for the human
   to correct in this session. Only then write, update `ingested:` and
   `updated:` in the frontmatter, and commit (repo targets).
10. **Close with routing** by project maturity:
   - `jobs-to-be-done` — core job undefined or contested, or new-job signals
     surfaced in the digest.
   - `research-synthesis` — a pile of evidence needs synthesis against the
     existing job set.
   - `discovery-plan` — framing still uncertain; unknowns need a plan.
   - `prd-writer` — feature-level scope is concrete enough to write.

   End with: **Next likely skill(s)** · **What to pass forward** (the
   `context.md` path + the ledger entries most worth resolving) · **Suggested
   next prompts** (2–3, plain language).

## No human present

The read-back requires a human. If invoked with nobody to answer, **escalate,
never guess**: write nothing durable beyond serialising your blocking questions
under `## Awaiting answers` in `context.md` (create the file with only
frontmatter + that section if it doesn't exist), and halt with a report. The
human answers inline and re-invokes; remove the section as answers are ingested.

## References

- `references/context-template.md` — the canonical `context.md` shape and the
  rules that bind every writer of the file.
