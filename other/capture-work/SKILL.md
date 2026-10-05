---
name: capture-work
description: Use this skill when a session has surfaced a list of future work — follow-ons, review recommendations, audit remediation items, deferred scope — and you want to capture it into workspace.toml so a later session can pick it up cold. Triggers on "capture this", "add these to the queue", "capture these as queue items", "queue these up", "add this to the backlog" + a bulleted or numbered list in context. Do NOT use to turn unstructured external input into a product brief (use author-brief), to decompose a brief into specs (use receive-brief), or to orient at session start (use workspace-status).
---

# Skill: capture-work

Classify-then-triage entry point for adding work to `workspace.toml`. Given a
bulleted or numbered list, `capture-work` classifies each item as `[build]` or
`[shape]`, derives spec paths, infers real dependencies, prioritizes and groups
the items, and writes them to the right destination — each entry carrying a
comment rich enough that a cold-start session can write the full spec without
revisiting this one.

`capture-work` writes `workspace.toml` only. It never creates spec files, and it
never invents a dependency. The user reviews the complete proposed change before
anything is written.

## Output rendering

Table — When presenting several items that share the same fields, render a Markdown table. Cap at ~5 columns; beyond that, switch to a per-item detail list. Right-align numeric columns.
Key–value / one record — For a single record's fields, use an aligned key: value list, not a two-row table.

## When to invoke

- A session produced a list of "things we should do later" — deferrals,
  follow-ons, recommendations, remediation items — and you want them queued.
- The items are concrete enough to name, even if not yet fully shaped.

If the input is unstructured external prose that needs shaping into a product
brief, use `author-brief`. If it is an already-written brief to decompose into
specs, use `receive-brief`. If you just want to see what is already queued, use
`workspace-status`.

## The destinations this skill writes to

`capture-work` appends only to the destinations it owns. For anything else it
*suggests* the right home and defers the write to the owning skill.

**Build items (`[build]`):**

1. **An active initiative's `[work].queue`** — well-shaped, ready build work
   scoped to an active initiative. If more than one initiative is `active`, ask
   which one; never guess.
2. **The repo-level `[backlog].open`** (no `type` field) — well-shaped, ready
   build work that is not initiative-scale. A **deferred acceptance criterion**
   of an existing spec also appends here, carrying a `source = "spec/<name> ACn"`
   key. `[backlog]` is a top-level, repo-durable section; if it does not exist
   yet, create it.

**Shaping items (`[shape]`):**

3. **An active initiative's `[shaping_queue].backlog`** — initiative-scoped
   shaping work, as `{slug = "...", type = "<subtype>"}`. Exception: `signal`
   subtype routes to `[shaping_queue].active` (ongoing monitoring context, not
   work to be picked up later).
4. **The repo-level `[backlog].open`** (with `type` field) — repo-level shaping
   work not scoped to an active initiative, as
   `{slug = "...", type = "<subtype>", needs?, source?}`. The `type` field is
   always present for shaping entries and never present for build entries.

## Procedure

### 1. Ingest

Take the bulleted or numbered list from context, or from what the user pastes.
Do not reject partial or messy input.

### 2. Classify

For each item, infer its mode:

- **`[build]`** signals: "implement", "fix", "refactor", "ship", "spec", "add",
  "migrate".
- **`[shape]`** signals: "research", "investigate", "assess", "map", "frame",
  "strategy", "design review", "competitive", "signal", "explore".

Surface the classification (`[build]` or `[shape]` + subtype) to the user as
part of the upcoming confirmation step. For `[shape]` items, infer the subtype:

| Subtype | Meaning |
| --- | --- |
| `shape` | Needs product-engineering shaping (the PE six-step process) |
| `research` | Needs desk research before implementation |
| `strategy` | Needs market/product strategy work |
| `signal` | Ongoing monitoring context — no discrete end state |
| `design` | Needs experience-design work |

Ask when the mode is ambiguous (some items straddle build and shaping). Ask when
the subtype is unclear. Never silently guess.

### 3. Derive slugs

For each item, propose a kebab-case `spec/<slug>` derived from the item text.
Check for collisions: if a spec directory with that slug already exists, or the
slug is already present in a `queue`, `active`, `shaping_queue`, or
`[backlog].open` list, stop and ask before proceeding — never overwrite.

### 4. Infer dependencies

Read the list for **explicit** sequencing language ("after X", "depends on Y",
"once Z ships", "then"). Add a `needs` edge only where the language is explicit,
using queue-prefix notation (`"work:spec/<slug>"`, `"backlog:<slug>"`). Items
the list does not sequence are independent — give them no `needs`.

**Never encode a priority *preference* as a `needs`.** A `needs` is a hard "cannot
start until" dependency. A preference about what to do first is queue order plus
a comment, not a dependency — a spurious `needs` would falsely serialize work
that could otherwise run in parallel.

### 5. Route

Decide the destination per item or batch using the classification from step 2
and the table in **The destinations this skill writes to** above.

For build items that fit neither `[work].queue` nor `[backlog].open` cleanly,
run the **escalation rubric** below and *suggest* the right home rather than
writing.

### 6. Prioritize

Two axes, never conflated:

- **Sequence** (`needs`) — hard dependency, from step 4.
- **Priority** — among items that are all ready, which to prefer first. This is
  advisory: it is expressed as **queue order plus a one-line rationale in the
  comment**, never as a schema field and never as a `needs`.

When two or more items are mutually independent and their order is a real call,
elicit priority from the user. Offer a ranking rubric as a prompt (for example
RICE, value-vs-effort, or the user's own decision matrix) — do not impose one,
and do not write a numeric score. Skip elicitation when dependencies already
determine the order or only one item is added.

### 7. Group

Pick the grouping shape by how tightly the items are coupled:

- **Independent batch** (default) — separable items land as flat entries under a
  single labeled comment header (e.g. `# Session audit YYYY-MM-DD — remediation
  batch`). Each stays its own entry so it can be picked up, sequenced, or
  parallelized alone. Annotate any parallel-safe set in the comment as advisory
  guidance ("items 2–4 are parallel-safe; do 1 first").
- **Atomic bundle** — when two or more items **must ship together** because
  splitting them leaves a broken intermediate state (the load-bearing case: a
  shared hard gate, where doing one without the other breaks a check), record
  them as a **single queue entry** whose comment enumerates the coupled parts
  *and* the coupling hazard. This is stronger than `needs`: `needs` orders two
  separately shippable items; an atomic bundle says there is no valid state
  between them. The tell is coupling language ("must ship together", "can't
  split", "would break if separate"). Confirm the bundling with the user.
- **Shaped work unit** — when the batch coheres as one outcome with a plausible
  appetite and an initiative fits, *suggest* `author-brief` instead of flat
  entries; the brief becomes the group container.

### 8. Compose comments

Each appended entry carries a comment block sufficient for a cold-start session
to write the full spec: **the problem, the fix, the affected file or skill, and
any key decisions already taken.** One-liners are not enough — write what a fresh
session would otherwise have to reconstruct.

For a `[backlog]` entry, also state the **unblock condition** — what must become
true before the item is workable ("Unblocks when: …"). Then cross-check it against
step 4: **if that condition is the completion of another *tracked* item — a
`[backlog]` slug or a `[work]` spec — as a hard prerequisite, add the matching
`needs` edge so the dependency is machine-readable, not prose only.** Do *not* add
a `needs` when the condition is disjunctive (satisfied by A *or* B — `needs` is
AND-only), names an entity not tracked in `workspace.toml`, or is an external event
(credentials provisioned, hardware available, a real-adopter session, "someone
takes the PR"). Those stay prose-only.

### 9. Confirm

Present the complete proposed change — entries (with their classification),
comments, order, inferred `needs`, and any escalation suggestions — and wait for
the user to approve before writing.

### 10. Write

Edit `workspace.toml` with a **comment-preserving** write — targeted text
insertion, or `tomlkit`. Never a full `tomllib` + `tomli_w` round-trip: it strips
every comment in the file, and the comments are the whole point.

- Append build entries to the resolved `[work].queue` or `[backlog].open` (no
  `type` field).
- Append initiative-scoped shaping entries to `["<ini-slug>".shaping_queue].active`
  (for `signal`) or `["<ini-slug>".shaping_queue].backlog` (all other subtypes).
- Append repo-level shaping entries to `[backlog].open` with a `type` field.
- If routing to `[backlog]` and the section does not exist, create it as a
  top-level `[backlog]` table with an `open` list and the standard header comment.
- Stage the file.

Degrade gracefully: if `workspace.toml` is absent, unparseable, or has no
matching queue, do not throw. Emit a diagnostic naming the derived entries and
how to add them by hand, and stop.

### 11. Hand off

For each `[shape]` item (non-signal), after writing, check whether the matching
skill is installed by probing for its `SKILL.md` under each adapter's installed
skill directory (pack is present if the probe succeeds in either location).

- **Pack present:** offer to invoke the matching skill in this session. If the
  user confirms, invoke it. If they decline, proceed.
- **Pack absent:** emit a named install hint: `requires <pack> pack — install to
  work this item`.

Always write the entry before the hand-off check. `signal` items skip the
hand-off entirely — they have no matching action skill.

Skill-to-subtype mapping:

| Subtype | Skill |
| --- | --- |
| `shape` | `frame-intent` |
| `research` | `desk-research-project-start` (desk-research pack) |
| `strategy` | `frame-situation` (PE pack); `frame-intent` as interim |
| `design` | `experience-status` (experience-design pack) |

Tell the user the items are queued and that `workspace-status` will surface them
at the next session start.

## Escalation rubric

When a build item does not cleanly fit `[work].queue` or `[backlog]`, suggest the
right home. The spine is one question: *is it shaped enough to become a spec
now, and at what scale?*

| Item shape | Suggest |
| --- | --- |
| Cluster of related features, one outcome + appetite, under an initiative | `author-brief` (brief queue) |
| Needs shaping, research, or strategy before it is a spec | classify as `[shape]` and route to the shaping queue |
| Big future feature, not yet shaped or scheduled | a row in `roadmap-intents.md` |
| Cross-cutting design question to work through | a row in `rfc-candidates.md` |
| Cross-cutting proposal needing a decision | `new-rfc` |
| Sustained, multi-quarter effort | standing up a new initiative (never auto-create) |

## Anti-patterns to refuse

- **Creating spec files.** This skill writes `workspace.toml` only.
- **Inventing a dependency.** Add `needs` only from explicit sequencing language.
- **Leaving a tracked hard-dependency as prose only.** If a `[backlog]` entry's
  unblock condition is the completion of another tracked item, it needs a `needs`
  edge (step 8) — not just an "Unblocks when" line. (Disjunctive, untracked, or
  external unblocks stay prose.)
- **Encoding a priority preference as a `needs`.** Preference is order + comment.
- **Writing a numeric priority or a new schema field.** Priority is order +
  comment; the schema is not extended beyond the `type` field for shaping entries.
- **Writing a `type` field on build entries.** `type` is shaping-only.
- **A full `tomllib` round-trip** that strips the file's comments.
- **One-liner comments** that a cold-start session cannot act on.
- **Overwriting** an existing spec directory or queue entry — prompt on collision.
- **Guessing the initiative** when more than one is active — ask.
- **Force-fitting** an item into an ill-matching initiative, or auto-creating an
  initiative or brief — suggest instead.
- **Hard-depending on an optional pack.** The hand-off is a conditional probe,
  never an import or a hard call.
- **Blocking on a missing `workspace.toml`.** Degrade to the named diagnostic.
