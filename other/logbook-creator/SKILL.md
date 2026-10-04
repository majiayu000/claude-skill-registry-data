---
name: logbook-creator
description: Design and create a logbook — a shared, queryable, schema-stable working surface that agents and humans append to, annotate, and query across sessions. Invoke when the user explicitly wants to track structured entries across multiple sessions or multiple contributors (e.g. "I want to track X across sessions", "I need a draft layer before committing to Jira", "let me review what the agent found before applying it", "multiple agents need to collaborate on this"). Also invoke when a document is accumulating repeated structured entries that would be better shaped as rows with named columns. Do NOT invoke for single-session analysis tasks, ad hoc data collection, or when the user asks to "collect" or "gather" information without mentioning cross-session reuse or multiple contributors — those are scratch tasks, not logbook tasks. This skill creates the logbook itself and a spec file — it does NOT create or modify skills. For wiring the logbook into a skill, hand off to skill-creator afterward.
---

# Logbook Creator

## What this skill does

This skill runs a guided conversation that produces two artifacts:

1. **A logbook instance** — the actual storage (CSV, JSONL, SQLite, spreadsheet, or markdown table) with the schema in place.
2. **A logbook spec** — a sibling markdown file (`<logbook-name>.logbook.md`) describing everything needed to operate on that logbook: schema semantics, identity rule, partial-row convention, correction rule, query patterns, validation rules, actions, and governance.

This skill does **not** write SKILL.md files. Wiring the logbook into a skill is skill-creator's job — the spec file is the handoff artifact between the two.

## When a logbook is the right answer

A logbook is shared structured state that outlives a single session. It earns its cost when the state is repeatedly read, written, or queried by different actors across sessions. It is not a document, not a tracker, not a log, and not scratch state. Before proceeding, confirm at least three of the following are true:

- **Multiple contributors** — more than one agent or human reads and writes the same state.
- **Schema-stable structure** — the shape is predictable enough that tools can query it without understanding the content. You can name the columns in under 30 seconds.
- **Tool-queried, not reread** — the common questions are answered by filtering, sorting, or aggregating, not by scanning the whole thing in context.
- **Outlives the session** — the state needs to be readable by a different agent or session later.

If fewer than three hold, push back gently and propose an alternative: a markdown doc, chat state, a typed handoff artifact, or a tracker like Jira. Don't build a logbook the user won't actually need. See `references/concept.md` for the full framing and the anti-patterns to watch for.

## The conversation flow

Run these steps in order. Don't ask every question at once — each step builds on the previous one's answers.

### Step 1 — Understand the motivation

Ask the user what's going on in plain language, not "what columns do you want." Listen for which of these five motivation patterns the situation matches (it may be a blend):

- **Tracking across sessions** — accumulating entries (decisions, observations, feedback) that the same person or a future agent will consult later.
- **Staging before commit** — shaping draft entries (Jira candidates, config changes, content drafts) in a permissive layer before pushing to a strict target system.
- **Human-in-the-loop review** — agents produce structured results and a human reviews, annotates, approves, or rejects before anything is applied downstream.
- **Multi-agent coordination** — several agents read and write the same structured state; the logbook is the shared contract between them (explorer writes findings, critic scores, estimator adds numbers).
- **Collection for later analysis** — gather structured data during work sessions now so that filtering, aggregation, or visualization is cheap later.
- **Driver / work-queue** — the schema *is* the todo list: an empty stage cell is the trigger for an agent to do that stage, and `WHERE <stage> IS NULL` is the work queue. No external orchestration list. This pattern has its own required gating — see Step 2.5.

Reflect back what you heard in one sentence: *"So this sounds like a staging surface — you want agents to shape candidates, and you review and push approved ones to X. Is that right?"* The motivation shapes everything downstream, especially which validation rules, actions, and governance defaults matter.

**Watch for the hidden logbook:** users sometimes say "I want a planning doc" or "I need a tracking sheet" when what they actually want is rows with structured annotations. If the user describes entries with statuses, scores, owners, or categories, test whether it's a logbook before defaulting to prose.

**Also watch for non-logbook problems.** If the work is truly single-session, single-reader, or still figuring out its shape, don't push a logbook on the user. Say so and suggest the lighter alternative.

### Step 2 — Scope & lifecycle

Before picking columns or a storage format, work through four sub-questions about where this logbook lives, how entries are partitioned, whether it will actually be used, and what state architecture it needs (2.1–2.4 below), plus a conditional fifth check (2.5) that fires when the logbook is a work-queue that drives agent work. Each sub-question feeds into the next and into downstream steps. Don't collapse these into one prompt — they build on each other, and users often revise their earlier answer once a later one forces the issue. Let them go back.

#### 2.1 Scope, location, lifetime

Ask in three probes, conversationally — not as a form. These three decisions reshape every downstream choice.

**Scope.** *"Is this logbook personal — living on your machine and read mostly by you — or shared — read and written by a team, multiple machines, or committed to a repo?"*

- **Personal** → Location defaults toward `~/.local/state/<name>/`, `~/.claude/skills/<name>/`, or another home-relative path. Governance defaults to single-owner, no access control. Conflict resolution trivial.
- **Shared** → Location defaults toward a repo path or a shared store (Google Sheets, shared SQLite). Governance must name an owner and access policy. Conflict resolution is non-trivial.
- **Ambiguous / blended** → Pick one and document the assumption. Mixed personal/shared is a governance trap; force the user to choose, or split into two logbooks with separate specs.

**Location.** *"Given that, give me an absolute path where this logbook should live."*

Validate the path pattern in conversation (save the filesystem check for Step 5):

- Reject ephemeral-looking paths when lifetime is longer than the session. Patterns that indicate ephemerality: `/tmp/…`, `/private/var/folders/…`, `/sessions/…`, any path under a sandbox or working directory whose stability across sessions is not guaranteed. When detected: call it out and ask the user for a durable path.
- Personal scope + path inside a git repo → warn: *"This will be committed unless gitignored. Do you want that? If not, either move to a home-dir path or plan to add a `.gitignore` rule right now."*
- Shared scope + path only on the local machine (e.g. `~/notes/…`) → warn: *"Only you will have this. To share, pick a committed repo path, a shared drive, or a hosted store."*

If no durable path is available (sandbox, fresh machine, no persistent storage), don't paper over it. Say so explicitly: *"This will be a session-scoped logbook; it won't survive a new shell."* Lifetime collapses to "session" and the Step 1 logbook-vs-scratch check applies again — a session-scoped logbook is usually scratch state.

**Lifetime.** *"How long does this need to be readable? One session, a sprint, a quarter, or indefinite?"*

Lifetime drives governance defaults in Step 5:

- **Session** — no sunset rule needed; logbook is scratch. Reconsider whether a logbook is the right shape at all (see Step 1 anti-pattern).
- **Sprint / quarter** — sunset rule is the end of that window.
- **Indefinite** — archival rule required (move to `archive/` after N days of no writes on a resolved entry, or similar).

End 2.1 with a one-sentence recap: *"So this is a personal|shared logbook at `<path>` that should last `<lifetime>`. Confirm before we partition."*

#### 2.2 Partitioning

*"One file holding all entries, or one file per X?"*

Present three common patterns tied back to the motivation from Step 1:

| Pattern | Fits | Filename shape | Notes |
|---|---|---|---|
| Single growing file | Tracking/staging motivations with one topic and modest volume | `<name>.<ext>` | Simplest. Good default. |
| One file per problem/topic | Multi-agent or debugging work where each topic has its own arc | `{YYYY-MM-DD}-{slug}.{ext}` (date = file creation) | Cross-topic queries become `csvstack *.csv` or globs. Columns that name the topic (`problem_id`, `topic`) become redundant and should be dropped. |
| One file per time window | High-volume or short-lived scopes (daily standup log, weekly retro) | `{YYYY-MM-DD}.{ext}` or `{YYYY-W##}.{ext}` | Similar effect on columns: drop `session` or `week`. |

Decision rule: if the user answers "one file per X," the filename scheme AND the redundant-column list are decided **here**, not in Step 3. Step 3 reads these answers and drops the redundant columns from each record type's schema, adding a one-line note below each affected table naming each dropped column and why.

Mixed partitioning (some entries shared, some personal; some per-topic, some global) is out of scope. Push the user to pick one, or to split into two logbooks with separate specs.

End 2.2 with the filename shape confirmed on an example path built from the 2.1 answer — e.g., *"So entries will live at `/Users/alice/.local/state/debug-log/2026-04-15-flaky-api-tests.csv`. Confirm."*

#### 2.3 Usage commitment

The hardest sub-step. The concept warns: *"Creating a logbook nobody reads"* is the most common anti-pattern. 2.3 is the upfront check for it.

Ask two questions, both requiring **concrete** answers:

**Append moment.** *"Walk me through the very next time you'd add an entry. When (what time of day, what trigger), by whom, and what prompts you to open the file?"*

Good answers are specific: *"Next debugging session, after I try a fix and it fails, I run `append-attempt`."* Bad answers are vague: *"Eventually, when I think of something."*

**Query moment.** *"Now walk me through the next time you'd read or filter entries. When, by whom, and what decision does the query inform?"*

Good answers: *"Before I start on a flaky-test problem, I run `query-before-trying` to avoid repeating approaches."* Bad answers: *"For reference sometime," "if I need it later."*

If either answer is vague, push back with one of:

- **Redirect to a lighter alternative.** *"That sounds like what a markdown doc / chat state / Jira ticket gives you. Want that instead?"*
- **Sharpen the motivation.** *"If you can't picture concretely appending or querying, reconsider: is this tracking, or would a short prose doc be a better fit?"*
- **Commit to a trial.** *"Let's build a minimal version anyway — but the sunset rule is `if no entries in 2 weeks, archive.` Agree to that?"*

Proceed to Step 2.4 when both the append and query moments are concrete, or after an explicit commit-to-trial with the sunset rule recorded in governance. (Step 2.4 — state architecture — still comes before Step 3; do not skip it.) If the user cannot describe either moment concretely and declines the trial option, recommend a lighter alternative (markdown doc, chat state) and stop.

If the user insists on the logbook despite vague answers, proceed — but record the vague answers verbatim in the spec's `## Governance` as *"Usage pattern not yet articulated; revisit after first week. Sunset after 14 days of no writes."* This documents the exception so a future reader can see the upfront check was skipped intentionally.

#### 2.4 State architecture

Before picking columns or tables, decide what kinds of state this workflow actually produces. Serious agent workflows often need more than one record type — a raw trace layer, a mutable ledger, a feedback layer — with different mutability rules. Skipping this step locks you into one-table-fits-all and forces bad trade-offs in Step 3.

Ask these seven questions in conversation (not as a form):

1. **Stable nouns** — *"What are the stable nouns in this workflow? Things like runs, hotspots, issues, candidates, feedback events, sources, sections — whatever the user's vocabulary names."*
2. **Append-only vs mutable** — *"Which of those are append-only (a new occurrence is a new row) and which hold mutable current state (the same thing gets updated as work progresses)?"*
3. **Cross-session recurrence** — *"Does the same real-world thing recur across sessions? The same issue reappears across PRs; the same candidate comes back in another run. If yes, a domain fingerprint is needed alongside the row key."*
4. **Raw vs surfaced outputs** — *"Are there raw model outputs and accepted/surfaced outputs? If so, do they need to live separately so dropped-but-reviewable candidates don't get thrown away?"*
5. **Later annotation** — *"Will humans or agents later accept, fix, dismiss, or suppress entries? If yes, there's either a feedback record type or a state field on the existing record type."*
6. **Smaller work units** — *"Is there a smaller meaningful work unit inside each artifact — a hotspot inside a run, a finding inside a hotspot, a claim inside a source? Nested hierarchies surface here."*
7. **Identity layers** — *"What identity layers does this workflow need? The common four are row key (unique per row — often one per record type in multi-entity designs), run-boundary key (scopes rows to an execution), domain fingerprint (a hash of the root-cause concept — enables semantic dedup across runs), and occurrence (how often the same fingerprint has appeared — tracked by fingerprint-count queries, not a separate column). Not every workflow needs all four."*

**Output decision.** Name whether this job needs a **single-table logbook** or a **multi-entity logbook**:

- **Single-table** → one record type dominates and the other questions collapse to "not really." Step 3 passes through 3A/3B trivially (one record type) and lands in 3C with a flat schema.
- **Multi-entity** → several stable nouns with different mutability rules, or raw-vs-surfaced separation, or cross-session recurrence. Step 3A names several record types, 3B iterates per type, 3C produces per-table columns.

Whether a multi-entity logbook also needs an append-only JSONL run-trace alongside its SQLite ledger is a Step 4 question (projections), not a separate branch here.

#### 2.5 Work-queue (driver) check

Run this gate for **every** logbook. Ask one question:

> *"Is an empty (NULL) cell in some column the signal for an agent to do work on that row?"*

If **no**, skip to Step 3. If **yes**, this is a **driver** (work-queue) logbook: the schema is a state machine and emptiness is a transition trigger. The five decisions below are **required gates, not optional probes** — skipping any one ships a queue that silently double-works, runs stages out of order, stalls, or loops forever. The dimension is orthogonal to single-table vs. multi-entity (2.4): a driver can be either.

First, a **pre-check (tracker gate):** a driver framing does **not** exempt the Step 1 "three of four" test. If per-person assignment, due dates, notifications, or staleness SLAs are present, this is work-management — **stop, redirect to Jira/Linear, and do not proceed to the five decisions.** The driver framing does not change that outcome. Otherwise, work the five decisions below. **Before working them, check yourself against the shortcuts in this table** — each feels reasonable in the moment and is wrong:

| If you catch yourself thinking… | Stop — the rule is |
|---|---|
| "The user said 'empty = todo', so I'll trigger on the empty content cell (`comment`, `summary`, `result`)." | A stage can finish successfully and still leave that cell empty. Trigger on a dedicated `<stage>_status` sentinel where **NULL means pending only** — never on a content column. *(Decision 1)* |
| "There's only one worker, so I don't need claiming." | Ask whether two workers could *ever* run at once. If yes or unknown, add the lease now — retrofitting concurrency onto a live queue is a mid-flight schema migration. *(Decision 2)* |
| "They're just columns to fill in; the order will sort itself out." | Elicit the stage dependencies and bake each prerequisite into that stage's ready-query. A bare `WHERE <stage> IS NULL` runs stages out of order. *(Decision 3)* |
| "Every row will complete eventually." | Some inputs never succeed (dead link, corrupt file, un-doable item). Design an attempts counter + a terminal *parked* state before first run, or one poison row starves the queue. *(Decision 4)* |
| "The lease makes a crashed worker's row reclaimable, so crashes are handled." | Reclaimable is recovery, not accounting. A crash never reaches the error branch, so an error-time counter stays at 0 and the row loops claim→crash→reclaim forever — invisible to any snapshot audit. Count attempts at claim time; the reclaim path parks (reaper). *(Decision 4)* |
| "It's a driver logbook, so the tracker test doesn't apply." | The driver framing exempts nothing. Per-person assignment, due dates, notifications, and staleness SLAs are work-management → redirect to Jira/Linear. *(Pre-check — see above)* |

The five decisions, each a required question:

1. **Sentinel — what does empty mean?** **Propose a `<stage>_status` column for every triggering stage by default** (`NULL` = pending; explicit `done`; plus any terminal values) — the trigger and every ready-query key off it, never the content column. The question *"Can this stage finish successfully and still leave its content cell empty?"* is **diagnostic, not a yes/no toggle for whether to add the sentinel.** Even if the user says a completed stage always writes content, keep the sentinel: empty-string and `NULL` are indistinguishable in a content column, and the sentinel costs nothing. Only omit it if the user gives a concrete reason the stage *literally cannot* produce a successful empty result — and when in doubt, keep it. If the user first answers "no, the content is always filled," challenge once with a counter-example (*"and if the agent looks and finds nothing worth recording?"*) before accepting. Carries into Step 3B as a partial-row carve-out.
2. **Concurrency — who claims a row?** Ask: *"Will more than one worker process rows at the same time?"* If yes/unknown: add `claimed_by`, `claimed_at`, `lease_until`; claim atomically; and every ready-query excludes leased rows (`lease_until IS NULL OR lease_until < :now`) so a crashed worker's row becomes reclaimable. Carries into Step 4 (atomic claim ⇒ SQLite, not CSV).
3. **Dependencies — what must be true before a stage runs?** Ask: *"Can these stages happen in any order, or must one precede another?"* Each stage's ready-query then includes its prerequisite (`<this>_status IS NULL AND <prior>_status = 'done'`), not a bare null-check. Even if only one stage is visible, ask whether any step must precede it or consume its output — implicit stages surface here, before the schema is fixed.
4. **Failure — what happens when a row can't be done?** Ask: *"If a worker errors on a row, does it retry, and how many times before giving up — and does a worker always survive to report its failure?"* Add `<stage>_attempts` (default 0) incremented **inside the atomic claim** — count claims, not reported errors: a worker that crashes or is killed never reaches its error branch, so an error-time counter stays at 0 while the row loops claim→crash→reclaim forever, invisible to any snapshot audit. Add a terminal `failed`/`parked` status, a ready-query predicate `<stage>_attempts < N`, a **reaper on the reclaim path** that parks exhausted rows at rest (parking must not depend on the worker reporting), and a parked-rows query that surfaces dead-letter rows for a human. Distinguish transient reported errors (release lease, retry) from terminal (park); silent crashes are bounded by the claim counter. Size `N` with headroom — benign interruptions also consume claims.
5. **Terminal outcomes — what stops a row advancing?** Some results are done-but-dead (`rejected`, `excluded`, `duplicate`). Name which status values advance a row and which absorb it, so the next stage's ready-query (decision 3) admits only genuinely-advancing rows.

Record the answers; they drive the schema (Step 3), storage (Step 4), and the driver spec sections (Step 5). For generic column/query templates and a full worked example, read `references/work-queue.md`. Then proceed to Step 3.

### Step 3 — Entity-first schema design

By this point Step 2.4 has decided whether this is a single-table or a multi-entity logbook. Both paths run through the same three sub-steps — single-table collapses them trivially (one record type) while multi-entity fans them out per record type.

Two answers from earlier still shape what gets recorded:

- **Partitioning (2.2).** If the user chose one file per X, drop columns whose values are encoded in the filename (`problem_id`, `session`, `topic`, `date`, `week`, etc.) from every record type that would otherwise include them. Annotate their absence with a one-line note under the affected table: *"Column `<name>` is encoded in the filename, not stored."* Keeping the column in a record type's schema and the filename both is redundant and invites drift.
- **Scope (2.1).** If the logbook is shared, `author` (or equivalent) is a required column on any record type a human or external agent writes. If personal, `author` can be optional and defaults to the single owner recorded in governance.

#### 3A — Derive record types

List the tables or record kinds before naming any columns. Examples: `review_runs`, `hotspots`, `candidate_findings`, `issues`, `occurrences`, `feedback_events`. For single-table logbooks this is trivial — one record type — but ask the question anyway so the decision is recorded rather than assumed.

#### 3B — For each record type, define

Answer each of these once per record type, grounded in the user's scenario rather than abstractly:

- **Purpose** — one sentence: what this record type is for.
- **Identity key(s)** — the row key. If Step 2.4 surfaced cross-session recurrence, add a domain fingerprint. If the record type is run-scoped, add a run-boundary key as well.
- **Mutability** — append-only or patchable current state. This usually falls out of the motivation: audit-sensitive record types append; refinement-heavy ones patch.
- **Partial-row convention** — empty string, explicit null, or "unknown". One convention per record type. Mixed conventions corrupt filters. **Driver carve-out (Step 2.5):** in a driver logbook, every `<stage>_status` column reserves `NULL` for *pending* exclusively and never accepts empty-string — a worker writing `""` to a status column is indistinguishable from pending and gets re-claimed forever. Content columns still follow the one-convention rule.
- **Correction rule** — append-only (new row supersedes) or patch-in-place. Must be consistent with mutability: append-only types correct by appending; patchable types correct by patching.
- **Relationships** — foreign keys into other record types, parent/child hierarchies, any cross-table link.
- **Suggested indexes** — for SQLite backends, propose indexes based on the expected query patterns for this record type (skip for CSV/JSONL).

If two contributors might mean different things by the same column name (`priority`, `status`, `score`), write one sentence of field semantics so the meaning is explicit — define it now, before 3C drafts the columns.

#### 3C — Columns

Only after 3B is settled. Propose a starter set per record type; let the user refine. Include one sentence of field semantics per column. If the schema for any record type can't be described in under 30 seconds, trim or reshape before proceeding. For a driver logbook (Step 2.5), each stage contributes a `<stage>_status` sentinel column (plus `<stage>_attempts` where failure handling was decided, and the shared `claimed_by`/`claimed_at`/`lease_until` lease columns when concurrent) — these are part of the starter set, not afterthoughts.

Also ask one actions question here while the motivation is fresh: *"Does this logbook need to feed an external system — Jira, Miro, a report, another agent? If so, name it."* Record the answer. This populates the `## Actions` section in Step 5 with real content instead of a placeholder. If the user says no external system, write "No actions defined." in the spec.

### Step 4 — Primary store + projections

First establish what is authoritative, then what views exist. One store is the source of truth; everything else is a derived view.

#### Authoritative store

Pick the format that fits the data and the downstream experience, not by default. Make one recommendation with a one-sentence rationale; let the user override.

| Format | When to pick it |
|---|---|
| **CSV** | Flat columns, short values, single writer at a time, want to open in Excel or grep from bash. Good default for ideation, flat decision logs, feedback collectors. Easy to chart later. |
| **JSON Lines (.jsonl)** | Optional or nested fields, schema varies row to row. Still appendable and greppable. Weak if you want column CLI ops. |
| **SQLite** | Need real queries (joins, aggregates, GROUP BY), row volume over a few thousand, multiple logbooks reference each other, concurrent writers, or a multi-entity design from 3A. Loses plain-text inspectability. |
| **Spreadsheet** (Google Sheets, Excel) | Humans are primary editors or reviewers. Visual sorting, filtering, comments. Ideal for human-in-the-loop review. |
| **Markdown table** | Tiny (under ~20 rows), hand-maintained, read more than written. Rarely right for agent-written logbooks. |

Narrow the table by the location picked in 2.1:

- **Inside a shared git repo** → prefer plain CSV, JSONL, or Markdown. They are diffable and reviewable in PRs. Deprioritize SQLite (binary, review-hostile) and spreadsheets (not in the repo at all) — unless you have concurrent writers or a multi-entity design, in which case SQLite's transaction safety and relational queries outweigh the diff cost.
- **Under a home-dir or local-state path** → all formats in the table remain viable. Pick on motivation and data shape.

The motivation biases the choice: staging and collection lean toward CSV or SQLite (diffable, chartable); human-review leans toward spreadsheet; multi-agent concurrent writers and anything multi-entity lean toward SQLite.

Migration is always available — start simple, upgrade when the pain signals (nested fields → JSONL; need joins → SQLite; need human UI → spreadsheet). Tell the user this so they don't over-engineer up front.

**Driver logbooks (Step 2.5) with concurrent workers** need atomic row claiming — one `UPDATE … RETURNING` that hands a row to exactly one worker. Plain CSV cannot claim atomically (two workers read the same empty row and both act on it), so a concurrently-claimed driver requires **SQLite** or an enforced single writer. This overrides the "deprioritize SQLite in a repo" guidance above: keep the live SQLite queue at a stable state-path and, if repo visibility matters, commit only an exported snapshot projection.

#### Projections (optional)

A projection is a view derived from the authoritative store. Writes go to the authoritative store; projections are appended or regenerated alongside it. Each projection has one of three roles:

- **run-trace** — append-only event log alongside the ledger (typically JSONL). Preserves the full execution record; not queryable relationally. Use this when the skill needs to preserve intermediate reasoning or event-level detail that the authoritative ledger tables don't capture — even when the ledger itself is append-only.
- **export-only** — read-only snapshot for human browsing (Google Sheets, Airtable, a rendered report). Regenerated from the authoritative store; never edited directly; never the source of truth.
- **mirror** — editable copy. Almost always wrong — it creates the "second place to update" anti-pattern. Flag it and push back unless the user has a specific operational reason.

**Visualization probe.** Ask once: *"Will a human want to watch this logbook's state as it fills — a dashboard or progress view?"* If yes, spec an export-only **render projection**: a script, not a page — `view = render(store)`, a pure read-only function of the authoritative store. The deliverable being a script is the point: a hand-authored page is stale after the next write and its numbers drift from the store (the second-source-of-truth anti-pattern in the view layer). Hold the render to the determinism contract: it reads only the store and its projections (e.g. a run-trace), renders the queries the spec already defines (funnel/partition, validation, dead-letter), takes any "now" as an **explicit parameter** — never the wall clock; same store bytes must yield the same page, and an as-of stamp comes from that parameter or the store's own timestamps — writes nothing but its self-contained output file, and is regenerated wholesale (output carries a `GENERATED — do not edit` header). If a run-trace snapshot is captured, that is a separate capture step *before* the render, never inside it — otherwise rendering twice records twice.

Two rules bound the probe:

- **Temporal rule.** The store decides what the view *can* show. A patch-in-place ledger renders current state only; a trajectory (progress-over-time chart) requires retained history — an append-only run-trace or transition timestamps, which is a store decision (2.4 / this step), not a renderer feature. Never chart a trend from a single snapshot.
- **Scope rule.** One logbook, one render script bound to that logbook's spec. *"Make it configurable for my other logbooks too"* is the universal-platform trap in the view layer — and a shared generator driven by a config registry is that trap in softened form, even though it feels like "reusable infrastructure." Reuse happens by copying the convention into the next logbook's own script and spec.

For the full contract, anti-rationalization table, script template, and a worked example, read `references/visualization.md`.

If it is unclear which store is authoritative, the design is not finished. Ask again before moving on.

### Step 5 — Create the two artifacts

Before writing either file, re-verify the absolute path from 2.1 is writable and non-ephemeral. The parent directory may not exist yet — that is fine and expected; you will create it. Test writability against the first ancestor that *does* exist rather than the (possibly missing) immediate parent:

```bash
p='<path>'; while [ ! -d "$(dirname "$p")" ]; do p="$(dirname "$p")"; done; test -w "$(dirname "$p")" && echo ok || echo not-writable
```

If this prints `not-writable`, stop and ask the user to create the directory or choose a different path — do not proceed with file creation. If it prints `ok` and the immediate parent of `<path>` does not exist, run `mkdir -p "$(dirname '<path>')"` before writing, and note in the spec's `## Address` section that the directory was created as part of setup. If the path matches an ephemeral pattern (`/tmp/…`, `/private/var/folders/…`, `/sessions/…`, or any sandboxed working directory), stop and ask once more, even if the user insisted during 2.1.

The spec's `## Address` section must carry the absolute path from 2.1 and the line *"When the user moves this file, update the address here."* — this is already in the template below; do not drop it.

Write both files to the user's selected folder (or to the workspace if no folder is specified). Names:
- `<logbook-name>.<ext>` — the logbook instance (e.g., `retro-observations.csv`).
- `<logbook-name>.logbook.md` — the spec.

For a spreadsheet backend, the "logbook instance" step is a set of setup instructions (headers to paste, column types to set) rather than a file — spell them out clearly in the spec and in your message.

**If any binding has `status: pending-auth`** (cloud backends requiring credentials), also write a third file:
- `<logbook-name>.logbook.local.yaml.template` — committed to the repo as a safe example showing the shape of local overrides (placeholder values only, no real IDs or emails).

Then tell the user: *"Copy `<name>.logbook.local.yaml.template` to `<name>.logbook.local.yaml`, fill in your real IDs, and add `*.logbook.local.yaml` to your `.gitignore`. Never edit the spec file (`*.logbook.md`) to activate a binding."*

When writing a spec with `pending-auth` bindings, always add this comment block immediately before the bindings section:
```yaml
# GOVERNANCE: This file is permanently read-only once committed.
# Never edit address or status here — store resolved config in a local gitignored override.
```

The template must follow this structure:
```yaml
# <name>.logbook.local.yaml — LOCAL OVERRIDES (never commit this file)
# Copy from <name>.logbook.local.yaml.template and fill in real values.
bindings:
  - driver: <driver>
    label: <label>
    address: <driver>://<PLACEHOLDER_ID>/<PLACEHOLDER_TABLE>?<auth_param>=<PLACEHOLDER>
    status: active
# Environment variables: list any env vars referenced in address fields
```

For SQLite, create the database file with the table defined and a companion `_meta` table containing schema, identity rule, partial-row convention, correction rule, owner, and lifetime. Also write the human-readable spec alongside.

## Spec file format

The spec is the handoff artifact for skill-creator and for any human reading the logbook later. Follow this template. Do not omit sections — if a section doesn't apply, say so explicitly in one line so future readers know the decision was deliberate.

```markdown
# Logbook: <name>

<one-sentence job description — what this logbook is for and who uses it>

## Address

<absolute file path, database path + table name, or spreadsheet share link>

When the user moves this file, update the address here.

## Storage

<format + one-sentence rationale for why this format fits the job. If any projections were specced (Step 4), list each: role (`run-trace` | `export-only` | `mirror`) and address — and for a render projection, the render script path, what it renders, and its temporal capability (current-state only, or trajectory via which retained history).>

## Schema

| Column | Type | Required | Semantics |
|---|---|---|---|
| id | integer | yes | Auto-incremented row identifier, stable across edits. |
| ... | ... | ... | ... |

## Identity

<rule: auto-increment, natural key of (X, Y), or UUID — and how new entries get their ID>

## Partial rows

<convention for missing fields: empty string, explicit null, or "unknown">

## Corrections

<patch-in-place OR append-correction — with one-sentence rationale tied to the job>

## Queries

Concrete, working snippets against this logbook's actual address. Group by intent.

### Filter by <column>
<bash/python/SQL one-liner that works against the actual file>

### Sort by <column>
<working snippet>

### Aggregate / group by <column>
<working snippet>

### Summary stats
<working snippet>

## Validation

<what "ready" means for an entry — required fields for commit, review completeness checks, etc. Include a snippet that finds incomplete entries.>

## Actions

For each external system this logbook feeds:

### <action name — e.g., commit-to-jira>
- **Purpose:** <one sentence>
- **Readiness check:** <what must be true of a row before it can be acted on>
- **Dry-run:** <how to preview without side effects>
- **Effect:** <what happens in the target system>
- **Patch-back:** <what column gets updated on the source row, e.g., `jira_ticket_id`>

If no actions are defined yet, state that explicitly.

## Governance

- **Access:** <who can append, who can patch, who can read>
- **Lifetime:** <sprint / quarter / indefinite>
- **Conflict resolution:** <last-write-wins via git, spreadsheet native, SQLite transactions, etc.>
- **Sunset rule:** <when lifetime expires: archive, collapse to summary doc, or renew>
```

The query snippets must be the **actual commands** that work against the logbook as created — not abstract examples. If the logbook is at `/work/retro.csv`, the filter snippet should be a working `awk` or `python` call against that exact path. This is what makes the spec directly consumable by skill-creator.

### Multi-entity variant

When Step 2.4 decided this is a multi-entity logbook, extend the template above as follows. Sections not listed here stay identical to the single-table template.

- **Storage** becomes **Physical stores** — lists the authoritative store first, then each projection with its role (`run-trace`, `export-only`, `mirror`) and address — and for a render projection, also the script path, what it renders, and its temporal capability, exactly as in the single-table `## Storage` clause.
- **Schema** becomes one `### <RecordType>` subsection per table, each with its own schema table.
- **Identity**, **Partial rows**, **Corrections** each become per-record-type subsections, one block per record type — so a reader can see the full contract for one table without scanning the whole spec.
- **Queries** remains flat but includes cross-table JOIN examples where relevant.

No new YAML frontmatter fields. The `bindings` block remains the only structured frontmatter, present only when auth config is needed.

Example skeleton for the expanded sections (record type names are illustrative — substitute the ones derived in 3A):

````markdown
## Physical stores

- **Authoritative:** <format> at `<absolute path or address>` — <one-sentence rationale>
- **Projection: <label>** — role: `run-trace` | `export-only` | `mirror` — at `<address>` — <purpose>

## Schema

### <record_type_1>

| Column | Type | Required | Semantics |
|---|---|---|---|
| ... | ... | ... | ... |

### <record_type_2>

| Column | Type | Required | Semantics |
|---|---|---|---|
| ... | ... | ... | ... |

## Identity

### <record_type_1>
<rule>

### <record_type_2>
<rule>

## Partial rows

### <record_type_1>
<convention>

### <record_type_2>
<convention>

## Corrections

### <record_type_1>
<rule>

### <record_type_2>
<rule>
````

### Driver variant

When Step 2.5 identified this as a driver (work-queue) logbook, extend the template with the sections below. Keep them generic to the stages the user actually named — do not invent stages.

- **Schema** — each stage adds a `<stage>_status` sentinel column (and `<stage>_attempts` where failure handling was decided); the lease columns `claimed_by`/`claimed_at`/`lease_until` are shared across stages when concurrent. In Step 5, alongside `CREATE TABLE`, emit one `CREATE INDEX` per `<stage>_status` + `lease_until` pair — that is the ready-query hot path.
- Add a **`## Stages`** section — one row per stage, naming its trigger, action, and outcome values:

```markdown
## Stages
| Stage | Ready when (predicate) | Action | Done | Terminal-skip | Parked |
|---|---|---|---|---|---|
| <stage> | `<stage>_status IS NULL AND <prior>_status='done' AND <stage>_attempts < N AND (lease free)` | <what the agent does> | `'done'` | `'<skip>'` | `'failed'` |
```

- **Queries** must include, against the real address: each stage's **ready-query**; one **atomic claim** per *agent-performed* stage (every such stage in the Stages table, not just the first; a human-performed stage carries no lease/claim) (`UPDATE … WHERE id=(SELECT … LIMIT 1) RETURNING …`, incrementing `<stage>_attempts` inside it); a **reaper** that parks exhausted rows at rest (`UPDATE … SET <stage>_status='failed' WHERE <stage>_status IS NULL AND <stage>_attempts >= N AND (lease expired or absent)`), run on the reclaim path or at the top of each poll pass; a **funnel** (per-stage `count(*)`, `UNION ALL`'d = live burndown); and a **parked-rows** query surfacing dead-letter rows for a human.
- If the **visualization probe** (Step 4) fired, the funnel/partition and parked-rows queries above are what the render projection visualizes — the driver's live burndown becomes a page, making completeness visible rather than just queryable. Same determinism contract; the lease/staleness comparisons take `:now` from the render's explicit parameter, never the wall clock.
- **Actions** become **internal stage-actions** (they advance rows inside the logbook) rather than external pushes: each stage's readiness check = its ready-query predicate; effect = sets the stage status + releases the lease; patch-back = n/a. An external push, if any, stays a normal Action with its own patch-back column.
- **Governance** records the lease duration and that the authoritative store is safe for claiming (SQLite transaction = safe; CSV under concurrent workers = unsafe).

The poller that turns these ready-queries into agent dispatches is **skill-creator's job**, not this skill's — the spec is the handoff, exactly as for non-driver logbooks.

## Handoff to skill-creator

After the two files are written, tell the user what to do next. Typical next steps:

- *"Want to wire this into a new skill? Run skill-creator and point it at the spec — it'll generate a SKILL.md that uses these query patterns and validation rules."*
- *"If you already have a skill that should use this logbook, run skill-creator in update mode and reference the spec file."*
- *"If you just want to use the logbook directly in a session, the query snippets in the spec are copy-pasteable."*

Do not try to generate a SKILL.md yourself — that is skill-creator's job, and duplicating it produces the unified-substrate anti-pattern the concept warns about.

## Anti-patterns to avoid

- **Building a universal logbook platform.** One logbook, one schema, one job. Reusable infrastructure (id formats, timestamp conventions) is fine; a universal domain schema is the trap.
- **Creating a logbook nobody reads.** If the only consumer is the agent that wrote it, it's scratch state, not a logbook. Step 2.3's usage commitment is the upfront check for this: if the user can't concretely describe append and query moments, it is almost certainly not the right shape — say so and suggest a lighter alternative (markdown doc, chat state, Jira ticket) instead of building anyway.
- **Using an ephemeral or unverified path as the logbook address.** Running `pwd` in a sandbox or a fresh shell and writing that path into the spec produces a logbook the user can never find again. Always ask for an absolute, durable path in Step 2.1 and re-verify in Step 5 before creating any files.
- **Hand-maintained second source of truth.** A logbook that sits alongside Jira or a doc that humans actually edit will rot. The logbook must be authoritative for its slice, or generated from one.
- **Premature extraction from prose.** If the document's value is in its argument, sequencing, or evolving reasoning, don't flatten it into rows just because the entries look row-shaped.
- **Over-engineering the first version.** Start with the lightest storage that fits. Migrate when the pain shows up. The concept and schema don't change across migrations — only the serialization does.
- **Committing personal auth state into a shared spec.** If the spec is committed to a repo, any `status: pending-auth` bindings must stay as placeholders. Resolved IDs, credentials, and `status: active` are personal config — store them in a gitignored local file (`<name>.logbook.local.yaml`, copied from the `.template` written in Step 5) or env vars, never in the spec itself. When writing a spec with `pending-auth` bindings, add this note to the bindings section: `# GOVERNANCE: This file is permanently read-only once committed. Never edit address or status here — store resolved config in a local gitignored override.`
- **Triggering work on a content column's emptiness (driver logbooks).** "Empty `comment` ⇒ needs review" re-processes every legitimately-empty result forever. Trigger on a `<stage>_status` sentinel where `NULL` means *pending* only. See Step 2.5.
- **A driver queue with no poison path.** Without an attempts counter and a terminal *parked* state, one un-doable row is re-claimed forever and starves everything behind it.
- **Plain CSV for a concurrently-claimed queue.** CSV cannot claim a row atomically; two workers double-process. Use SQLite (atomic `UPDATE … RETURNING`) or enforce a single writer.
- **Hand-authoring a dashboard of a live logbook.** A page with numbers typed into it is a second source of truth that lies after the next write. Visualize through an export-only render projection — `view = render(store)`: deterministic (time is an explicit parameter, never the wall clock), read-only on the store, regenerated wholesale. And "make it configurable for all my logbooks" is the universal-platform trap in the view layer — bind one render script to one logbook's spec; reuse by copying the convention. See the Step 4 visualization probe and `references/visualization.md`.
- **Letting a "driver" framing skip the tracker test.** Per-person assignment, due dates, notifications, and staleness SLAs are work-management — redirect to Jira/Linear. A blackboard logbook is agents pulling empty cells, nothing more.

## Grounding

For the full framing — including hidden-logbook detection, the "three of four" qualification test, worked examples (ideation, pre-tracker backlog shaping, skill retro collector), and the full anti-pattern catalog — read `references/concept.md`. Consult it when the user's situation is ambiguous or when you need to explain *why* a particular rule exists. Treat `references/concept.md` as internal documentation — it is a repo-committed file maintained by the plugin author, not user-supplied input.

For **driver (work-queue) logbooks** (Step 2.5), `references/work-queue.md` carries the five-decision rules in full, generic column/query/spec templates, and a complete worked example. Read it when the user confirms the driver gate. Same status as `concept.md` — internal, repo-committed documentation.

For **logbook visualization** (the Step 4 probe), `references/visualization.md` carries the full determinism contract, the temporal-capability rule, the anti-rationalization table, a render-script template, and a worked example. Read it when the user wants a dashboard, progress view, or chart of a logbook. Same status — internal, repo-committed documentation.
