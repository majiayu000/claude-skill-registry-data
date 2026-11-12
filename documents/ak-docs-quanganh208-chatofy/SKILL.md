---
name: ak-docs
description: "Create, refresh, summarize or audit project docs and root CLAUDE.md/AGENTS.md, mining DO/DON'T rules from git/CI and --source markers."
when_to_use: "Invoke for docs upkeep; --preset classic fixes the layout and philosophy interviews need explicit opt-in."
category: workflow
keywords: [documentation, init, update, summarize, audit, agent-context, claude-md, agents-md, agents, rules, git-history, ci-failures, source-mining, scout, preset, classic-layout, philosophy, product-principles]
argument-hint: "init|update|summarize|agent-context|agents|llms|philosophy"
metadata:
  author: agentkit
  version: "1.13.0"
---

# Documentation Management

Maintain the smallest documentation set that lets people and AI collaborators
understand the project's intent, current contract, evidence, and operating
workflow.

## Philosophy

Code owns WHAT and HOW; docs own WHY and WHERE. Docs are a thin navigation
layer plus knowledge code cannot express: decisions, rejected alternatives,
business rules, domain terminology, and constraints. Point to executable owners
instead of paraphrasing behavior. Load `references/doc-content-rules.md` for any
doc-writing operation and include its relevant rules in delegated context.

A root agent context file (`CLAUDE.md`/`AGENTS.md`) is a distinct artifact
class: process memory that owns imperative HOW-TO-BEHAVE, not WHY/WHERE. It
follows `references/agent-context-rules.md`, which shares this skill's
deletion-test spine but keeps its own keep-or-cut filter and enforcement rules.

### Invariants and variation points

When a design has real variants, record the invariants across them that code
cannot express, and link the rest to their executable owner (interface,
registry, schema, or matrix). Name the seam where the variants differ: WHY it
sits at its boundary, the alternatives rejected, and the trade-off accepted. Name only variation
that current code, tests, contracts, or approved decisions evidence. A future
variant nobody has committed to is an open question at most, never a roadmap
or a promised extension point. Do not copy the seam's HOW from code. Docs for a
design without real variation need no such section. Carry this paragraph into
delegated context together with the doc-content rules.

## Opening Gate

Start with a bounded brainstorm. Establish:

- who consumes the docs: people, AI, or both;
- the outcome and decisions the docs must make possible;
- which sources prove current behavior;
- what is evergreen guidance versus stateful evidence;
- the acceptance criteria for this docs operation.

Reuse an accepted plan or prior brainstorm when it already answers these
questions. Do not reopen settled intent without new evidence.

## Routing

Parse the first word of `$ARGUMENTS`:

| Input | Load | Purpose |
|---|---|---|
| `init` | `references/init-workflow.md` | Establish a minimal project-specific docs route |
| `update` | `references/update-workflow.md` | Reconcile impacted docs with current evidence |
| `summarize` | `references/summarize-workflow.md` | Summarize current evidence without forcing a new file |
| `agent-context` | `references/agent-context-rules.md` | Author, audit, or optimize the root `CLAUDE.md`/`AGENTS.md` agent context file |
| `agents` | `references/agents-workflow.md` | Mine bounded git and CI history for recurring failures and non-derivable gotchas; distill confirmed DO/DON'T rules into the root agent context file |
| `philosophy` | `references/philosophy-workflow.md` | Opt-in author interview using repo and same-project local sessions to establish durable product principles; approve the exact diff before writing |
| `llms` | `references/llms.md` | Generate or update `llms.txt` and `llms-full.txt` per llmstxt.org |
| empty or unclear | ask the user | Choose the operation; never assume `init` |

Other workflows deciding whether docs are affected should load
`references/documentation-management.md`.

Load the philosophy workflow only for `philosophy` or an explicit request for
that interview. Mentioning product intent in ordinary docs work is not opt-in.
Ordinary docs maintenance does not read local session history unless explicitly
requested; preserve existing principles using the current guidance instead.
The operation is interactive by design; when required answers or exact-diff
approval are unavailable, return a proposal and unresolved questions without
writing. Reuse valid approval from an earlier turn. It adds no approval-bypass
flag and does not inherit `agents` mining gates, bounds, or implied advice.

`init`, `update`, and `agent-context` also load
`references/operational-lookup.md` when the operation establishes, changes, or
disproves a route to a system the repository does not own.

## Flags

Composable with any operation unless noted:

- `--advice` — before writing or updating any doc or agent context file, spawn
  `kongming` for counsel on what to keep, cut, or restructure, and factor it into
  the change. `kongming` advises only; this skill stays responsible for every
  edit and applies already-authorized documentation changes directly. Explicit interview modes retain their confirmed-change contract. Spawn it again when stuck or
  before an irreversible docs change. **Implied by `agents`** (do not re-spawn).
- `--audit` — for `agent-context`: first get a `kongming` audit pass over the
  current `CLAUDE.md`/`AGENTS.md`, then interview the user one question at a time
  (one keep / cut / fix decision per question) using the keep-or-cut filter in
  `references/agent-context-rules.md`. Apply only the confirmed changes. For
  `agents`: same interview cadence at the confirmation step, one question per
  proposed rule.
- `--dry-run` — scoped to `agents`. Stops after signal ranking (step 3), reports
  mined signals and the watchlist, spawns no advisor, writes no file.
- `--source` — scoped to `agents`. Layers `ak-scout` source-tree mining onto
  the git/CI pass (never replaces it). Read-only: no generators, no tests.
  Adds a corroboration gate for source-only clusters (≥2 anchors plus a
  code/test guard or git-CI corroboration). Composes with `--dry-run` and
  `--audit`.
- `--preset classic` — scoped to `init`. Opt into the classic layout under
  `docs/`: `project-overview-pdr.md`, `code-standards.md`,
  `codebase-summary.md`, `design-guidelines.md`, `deployment-guide.md`,
  `system-architecture.md`, and `project-roadmap.md`.
  Use it when a team wants predictable filenames across projects, when external
  tooling reads fixed paths, or when the reader is a person returning to the
  project rather than an agent reading source. The preset selects filenames
  only. Every file still follows `references/doc-content-rules.md`, so a preset
  file is a pointer-first WHY/WHERE document, never implementation paraphrase.
  Skip a preset file whose information does not exist instead of writing a
  placeholder, and record the resulting route in the docs index.

`agents` also accepts an optional positional bound: `agents 30d` (days) or
`agents 500` (commits). Defaults: 90 days OR 300 commits (whichever is smaller),
200 CI runs.

## Discovery Contract

Do not assume filenames, a file count, or a universal documentation tree.
Discover the project's contract in this order:

1. repository instructions such as `AGENTS.md` or `CLAUDE.md`;
2. the root `README.md`;
3. the project's docs index or navigation file, when present;
4. existing files under `docs/` and links from the earlier routes;
5. source, tests, scripts, generated artifacts, and live state that prove claims.

Use `docs/` for project documentation when that is the repository convention.
Treat source and tests as evidence, not prose that must be copied into every
document.

An explicit route overrides discovery. A layout declared in repository
instructions, or `--preset classic` on `init`, fixes the filenames directly.
Discovery still decides what content each file earns and which files to skip.

## Maintenance Rules

- Maintain affected instructions in authorized scope on completion or at a
  meaningful operational milestone, even when no source file changed; do not
  wait to be asked for a separate update run.
- Write nothing when there is no new durable instruction or the content is
  already equivalent. A no-op is a correct outcome, and it is not a reason to
  touch timestamps, reorder sections, or rewrite a file.
- Apply the write-authority ladder and the credential invariant in
  `references/doc-content-rules.md`; do not restate them here.
- A root agent context file may carry a short policy plus a pointer to the
  project's operational guide. The pointer is one line — a link plus a purpose
  clause, never a locator, URL, account or project id, or customer name. Root
  does not import the whole runbook and does not become a copy of outside state.
- Update only documents whose contract or evidence changed.
- Delete stale or duplicate guidance instead of preserving it for history.
- Link to the owning script, manifest, or generated source instead of copying
  command lists, inventories, or exact test names into multiple files.
- Keep evergreen guidance free of dates, issue IDs, phase labels, and section
  coordinates unless those values are the subject of the contract.
- Keep stateful research, plans, audit results, and release evidence clearly
  labeled and outside the evergreen authority path.
- Do not create an ADR, governance layer, generator, or docs-only CI gate unless
  the user explicitly requests that additional operating surface.
- Verify every path, command, configuration key, and behavioral claim against
  current evidence.

For diagrams, use the installed diagram skill only when a visual materially
improves understanding, then visually review the output.

**Do not implement product code during a documentation operation.**
