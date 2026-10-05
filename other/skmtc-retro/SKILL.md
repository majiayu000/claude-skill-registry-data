---
name: skmtc-retro
version: 0.2.0
description: |
  Run a self-retrospective on a SKMTC-related session — generator
  authoring, CLI configuration, debugging, or any sustained interaction
  involving `@skmtc/core`, `@skmtc/cli`, or `@skmtc/gen-*` packages.
  Captures three distinct outputs: (1) friction entries (mistakes,
  surprises, overridden defaults, multi-cycle struggles), (2) a
  "knowledge acquired" block recording facts the agent learned during
  the session that weren't in its training — the primary signal for doc
  gaps — and (3) a closing priority list ranking the top 2-3 findings
  for docs/skills triage. Wins are logged only when they identify a
  pattern worth codifying that isn't already in a skill.

  Use this skill when the user asks to "retro", "skmtc retro", "log
  friction", "reflect on this session", "what did we learn", "run a
  retrospective", or after substantive SKMTC work (generator authoring,
  multi-step debugging, non-trivial CLI configuration) where capturing
  observations would help improve skills, docs, or SKMTC itself.

  Distinct from the `skmtc-cli` and `skmtc-generator` skills — those
  guide *doing* the work; this skill captures observations *about* the
  work. Do not invoke this skill during ordinary work; it is end-of-
  session (or mid-session-checkpoint) only.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  internal: true
---

# SKMTC retro

Capture the three categories of output only the LLM can produce —
friction entries, knowledge acquired, and a priority ranking — and
write them to a per-session file so they can be reviewed and acted on.
The primary goal is actionable signal: what broke, what was unknown,
and where to spend effort next. Wins are secondary and only worth
logging when they identify something uncodified.

## 1. When to invoke

**Run a retro after substantive SKMTC work:**

- Authoring a new generator (scaffold → working output)
- Cloning a stock generator and editing it
- Multi-step debugging of a failing generation
- Non-trivial CLI configuration (multi-generator setup, complex enrichments)
- Any session that involved 3+ generate-test cycles

**Skip retros for:**

- Quick lookups or single-command tasks
- Sessions that ended in immediate success with no friction
- Re-runs of work already covered by an earlier retro file

**Always retro when:**

- The user explicitly invokes this skill (any session length)
- The user asks "what did we learn?", "retro this", or similar

## 2. Locate the friction-log directory and pick a filename

The canonical location:

```
<skmtc-root>/skmtc/deno/docs/friction-log/
```

`<skmtc-root>` is the directory containing `skmtc/` and `skmtc-generators/`.
To resolve:

1. Walk up from the current working directory looking for a
   `skmtc/deno/docs/friction-log/` directory.
2. If `<skmtc-root>` cannot be located, ask the user where the
   friction log lives or whether to create one. Do not silently
   default to a fallback path.

### Filename convention

Each retro produces **one file per session**, named:

```
<YYYY-MM-DD>-<short-summary>.md
```

- `<YYYY-MM-DD>` — ISO date (today's date in the session's local time).
- `<short-summary>` — 3-4 word kebab-case description of the session's
  primary topic. Lowercase, hyphen-separated, no trailing date or
  numbers unless needed for disambiguation.

Examples:

- `2026-05-12-create-retro-skill.md`
- `2026-05-13-shadcn-form-clone.md`
- `2026-05-14-enrichment-design-spike.md`
- `2026-05-15-debug-empty-output.md`

The summary should capture **what makes this session distinct** from
others on the same date. Pick the dominant topic if a session covered
multiple areas; entries inside the file can still span several
concerns.

### Same-date collisions

If a file with the proposed name already exists (same date, same
topic), **append entries to that file** rather than creating a
duplicate. If a session on the same date has a genuinely different
topic, use a different summary so the filenames differ naturally
(e.g., `2026-05-12-create-retro-skill.md` and
`2026-05-12-shadcn-form-spike.md` coexist).

### One session = one file. No batches inside a file.

Entries are added **continuously** as observations occur, not
batched into rounds. Do **not** introduce `## Round N: <topic>` or
`## Pass N: <topic>` sections inside an entry file — they impose a
chronological-batch structure on top of the already-stable
per-entry numbering and make the file harder to skim.

When work genuinely splits into distinct phases — different scope,
different day's focus, different audit pass — that's a signal you
have **separate sessions**, and each warrants its own file with a
distinct `<short-summary>` slug. Examples for the same date:

- `2026-05-12-tutorial-docs-audit.md`
- `2026-05-12-claude-md-audit.md`
- `2026-05-12-how-to-docs-audit.md`

This is preferable to one `2026-05-12-docs-audit.md` carved into
`## Round 1`, `## Round 2`, `## Round 3`. Each file remains
self-contained, its index reflects only its own entries, and
cross-file references (`<filename>#<N>`) handle any genuine
linkage between sessions.

The rule is forward-looking — existing legacy files that use
round-N sections do not need to be retroactively split unless their
content is being substantially edited.

### Reading existing files

Before writing, **read any existing file you'll be appending to** to
match its numbering and avoid duplicate observations. You do **not**
need to read every file in the directory — each file is self-contained
and entries don't cross-reference unless explicitly stated.

## 3. The reflection prompts

The most valuable observations are ones a human reviewer of the final
code cannot reconstruct. Before drafting entries, work through these
questions explicitly. They are the leverage of this skill.

### For friction

- What **surprised** you? (API shapes, method-vs-property, error
  messages, behaviour that didn't match expectation)
- Where did you **override a default suggestion** from training data?
  (E.g., you almost wrote a config flag, but cloned instead.)
- What did you have to **guess** about? (Naming conventions, file
  layout, where a helper lives, which method to call.)
- Where did you **spend multiple cycles** fighting the same thing?
- What did you write that **felt non-idiomatic** — a sense that SKMTC
  has a better way that you couldn't find?
- Where was an **error message unhelpful** for diagnosing the cause?
- What **invariant** did you almost violate and have to back out from?

### For wins (high bar — codification candidates only)

Win entries are not "this felt smooth." They are "I observed a pattern
that should be the prescribed approach and isn't written down yet." Log
a win only when you can answer yes to: *If another agent did this task
tomorrow without this observation, would they likely do it wrong?*

- What pattern did you use that **isn't yet codified** in a skill or
  doc, but clearly should be?
- Where did the architecture or type system **enforce a correct
  approach** in a way worth teaching explicitly?

If nothing passes this bar, omit the wins section entirely. A session
with zero wins is normal and preferable to fabricated signal.

### For knowledge acquired

This is the highest-value section for improving docs. Ask: *What do I
now know about SKMTC that I did not know at the start of this session?*
These are not friction entries — they are knowledge-gap closures.

- What **API shape, method signature, or runtime behaviour** did you
  have to discover by trial or reading source, rather than from docs or
  training data?
- What **naming convention, file layout, or configuration key** was
  absent from training data and had to be inferred?
- Where did you rely on **analogy from another framework** that turned
  out to be wrong or only partially correct?
- What **constraint or invariant** did you not know existed until you
  hit it (e.g., single-base rule, location-independence requirement)?
- What would you want to **tell the next agent** doing this task that
  isn't written anywhere?

Capture each item concisely — the table format in §4 is designed for
this. Include the implication for docs: "this belongs in the generator
skill," "this needs a how-to doc," "this is a missing API reference
entry," etc.

## 4. File format

The session file structure:

```markdown
# <YYYY-MM-DD> — <Session topic>

<1-2 sentences describing what work was happening in this session.>

## Knowledge acquired

<1 sentence framing what domain this session operated in.>

| # | What I learned | Doc implication |
|---|----------------|-----------------|
| K1 | <concise fact — API shape, constraint, naming rule, invariant> | <skill / how-to doc / API reference / none> |
| K2 | ... | ... |

*If nothing genuinely new was learned, write: "No new SKMTC knowledge
acquired this session — all patterns matched prior training or
existing documentation."*

## Index

| # | Entry | Severity | Status |
|---|-------|----------|--------|
| 1 | <Entry heading> | friction | open |
| 2 | <Entry heading> | win | open |

---

### 1. <Entry heading> [severity]
...

### 2. <Entry heading> [severity]
...

---

## Priority for docs/skills

Top findings from this session, ranked by leverage for improving docs,
skills, or SKMTC itself. The user uses this list to decide what to act
on first — be specific about the action path.

| Rank | Entry | Why it matters | Action path |
|------|-------|----------------|-------------|
| 1 | #N — <heading> | <one sentence> | skill update / how-to doc / API reference / SKMTC code |
| 2 | ... | ... | ... |

Limit to 3 entries. If fewer than 3 stand out, list only those that do.
```

### The Index

The `## Index` block sits between the session description and the
first `---` divider. Its purpose is to let a reader (agent or human)
scan the file's contents and the status of every entry in seconds,
without paging through the body.

Index rules:

- **One row per entry**, in the same order as the entries themselves.
- **`#` column** matches the entry's stable number from §"Numbering".
- **`Entry` column** is the entry's heading text **without** the
  trailing `[severity]` tag (severity gets its own column). Truncate
  with `…` if the heading exceeds ~80 characters; the body is the
  authoritative version.
- **`Severity` column** is the bare tag (`blocker`, `friction`,
  `polish`, `win`) — no brackets.
- **`Status` column** mirrors the entry's `**Status:**` field
  verbatim, but condensed. Typical values:
  - `open` — unresolved
  - `resolved <YYYY-MM-DD>` — resolved on that date (optionally with
    a commit/PR ref, e.g., `resolved 2026-05-15 (PR #142)`)
  - `superseded by <filename>#<N>` — observation rolled into a later
    entry
  - `wontfix` — explicitly closed without action

The index is **derived data**: every value must match what's in the
body. When the two disagree, the body is the source of truth and the
index is wrong — fix the index.

### Maintaining the index

The index must be updated **every time the body changes**:

- **Adding an entry:** append a new row with the next sequential `#`,
  matching heading, severity, and `Status: open`.
- **Resolving an entry:** update the body's `**Status:**` line first,
  then mirror the change to the matching index row.
- **Editing an entry's heading or severity:** update both places in
  the same edit. The body and index must never drift.

If you only have time to update one of the two, update the body. A
correct body with a stale index is recoverable; a stale body is not.

### Entry format

```markdown
### N. <Descriptive heading> [severity]

<Concise context — what part of the work this was observed in.>

**What happened:** <concrete description, with code/commands where
relevant>

**What was expected:** <the assumption that turned out wrong; omit if
not applicable, e.g., for wins>

**Why it matters:** <the underlying principle the friction violates,
or the pattern the win exemplifies. This is the highest-value field —
spend the most effort here.>

**Possible fixes:** <open-ended; 1–3 suggestions if obvious, or
"unresolved — needs reflection" if not. **Do NOT pre-commit to a
category of fix** (skill change vs doc change vs code change). Leaving
this open encourages contemplation during periodic review rather than
locking in the first idea.>

**Version anchor:** `@skmtc/core@<version>`, `@skmtc/gen-<name>@<version>`
(record whatever generators and core version the observation was made
against)

**Status:** open
```

### Severity tags

- `[blocker]` — no workaround found; session got stuck
- `[friction]` — workaround exists; cost real time/cycles
- `[polish]` — annoying but not blocking
- `[win]` — a pattern worth codifying that isn't already in a skill
  or doc. Not "this worked well" — only "another agent would likely
  do this wrong, and the correct approach isn't written down."

Apply `[win]` sparingly. A session with no wins is normal. If
everything that worked smoothly is already codified, don't log it.

### Numbering

Entries within a single file are numbered sequentially starting at 1.
Numbers are stable **within the file** — once assigned, they don't
change. Cross-file references use `<filename>#<N>` format, e.g.,
"see `2026-05-12-create-retro-skill.md` #2".

There is no global numbering across files. Each session file is
self-contained.

## 5. What NOT to log

- Operational principles already documented in `llms.md` or the
  `skmtc-cli` / `skmtc-generator` skills — those are already captured;
  logging them is noise. **Exception:** if the doc exists but you
  couldn't find it, log that as a discoverability gap in `## Knowledge
  acquired` — the doc's existence doesn't mean it's working.
- Trivial typos or one-line corrections that aren't part of a pattern.
- Domain-specific decisions from the consumer project (e.g., the
  naming of a field in someone's app) — only observations about SKMTC
  itself.
- Things the user already explicitly flagged during the session.
- "I made a mistake" without a SKMTC-level lesson — a tutorial gap, a
  skill gap, an API surprise, or a generalisable pattern is what makes
  an observation worth logging.

If a session genuinely produced no new observations beyond what's
already in the log or the skills, **say so explicitly** rather than
inventing entries to fill the retro. False signal is worse than no
signal.

## 6. Entry length

Trivial observations: 1 paragraph. Subtle patterns: 2–3 paragraphs,
sometimes with a code example or comparison table. The log's value
comes from specificity, not brevity. Length should match what's
needed to make the entry reproducible by someone reading it months
later.

## 7. Composing the retro

The full flow:

1. **Generate the filename** for this session: `<YYYY-MM-DD>-<short-summary>.md`
   using today's date and a 3-4 word kebab-case description of the
   session's primary topic.
2. **Check** if the file already exists (same-date, same-topic
   continuation):
   - If yes: read the existing file, note the highest entry number
     and the current state of the `## Index` block, prepare to append.
   - If no: prepare to create a new file with the session header and
     an empty `## Index` table (§4 "File format").
3. **Reflect** — mentally walk through the session, applying the
   reflection prompts from §3. Distinguish genuinely new observations
   from things already captured.
4. **Draft the `## Knowledge acquired` table** — what you now know
   that you didn't know at session start (see §3 "For knowledge
   acquired"). Be concise per row. Include doc implication. If nothing
   qualifies, write the explicit "nothing new" note from §4.
5. **Draft entries** — friction first, then wins (only if they pass
   the codification bar from §3) — using the format from §4. Number
   sequentially from the current high-water mark (1 if new file).
6. **Draft the `## Priority for docs/skills` table** — pick the top
   2-3 entries (friction or knowledge items) by leverage. One sentence
   per entry on why it matters. Specify the action path.
7. **Write** the file (create or append). Do not modify earlier
   entries. **Update the `## Index` block in the same write** to
   include a row for every new entry. If you're appending to an
   existing file whose index is missing or out of date, rebuild it
   from the body in the same pass — the index must always match the
   body when you finish.
8. **Summarise to the user** in one short message:
   `Logged N entries (X friction, Y wins) to <filename>. Knowledge acquired: K items. Top priority: <entry heading>.`

## 8. Examples

### High-value knowledge acquired row

```markdown
## Knowledge acquired

Working on a cloned `gen-shadcn-form`, registering imports and fields.

| # | What I learned | Doc implication |
|---|----------------|-----------------|
| K1 | `register({ imports })` accepts string OR object `{ name, alias?, isType? }` per import. String and object are NOT equivalent — object form always produces `name as alias` output even when alias is omitted. | Missing from generator skill §import-registration; needs a note + example |
| K2 | The single-base rule (one factory base per package) applies to cloned generators too — cloning doesn't grant an exception. | Already in memory, but not in SKILL.md; add to §generator-constraints |
```

### High-value entry (LLM-unique observation)

> ### 6. `ImportNameArg` shape is overloaded with no warning [friction]
>
> Working on a cloned `gen-shadcn-form`, registering imports for field
> components.
>
> **What happened:** The `register({ imports })` API accepts either a
> plain string or an object `{ name, alias?, isType? }` per import. I
> assumed the object shape was a richer-spec-string — passed
> `{ name: 'TextField', isType: false }` to mark a plain non-type
> export. The output became `import {name as TextField} from '...'`
> instead of `import {TextField}`.
>
> **What was expected:** that `{ name: 'TextField', isType: false }`
> would be equivalent to the bare string `'TextField'`.
>
> **Why it matters:** the object shape is a footgun for the most
> common case (plain non-type import). The semantic difference between
> string and object is invisible from the type signature.
>
> **Possible fixes:** unresolved — the engine could normalize
> `{ name: 'X', isType: false }` to `'X'`, or the skill could warn
> against this shape, or the type could be tightened so only `isType:
> true` is acceptable in object form.
>
> **Version anchor:** `@skmtc/core@^0.3.7`, `@skmtc/gen-shadcn-form@0.0.55`
>
> **Status:** open

### Low-value entry (already documented; don't log)

> ### 7. `as` casts not allowed in production code [friction]
>
> Tried to use `as Schema` to satisfy types. The user pointed out the
> codebase prefers type guards.

This is already in the `skmtc-generator` skill's operational
principles table. Logging it adds noise without signal.

## 9. After the retro

Retro files are append-only for **entry bodies**. The user reviews
them daily and decides whether each entry becomes a skill update, a
doc update, a SKMTC code change, or a deferred reflection point. Do
not pre-commit to those resolutions in the entry — leave the
"Possible fixes" section open-ended. When an entry is resolved, the
user (or the skill, on its next pass through the file) updates **two
places** with the resolution date and a link to the relevant commit
or PR:

1. The entry's `**Status:**` line in the body.
2. The matching row in the `## Index` table.

The index and body must remain in lockstep — see §4 "Maintaining the
index".

If you notice during the retro that **the skill itself** has a gap (a
missing reflection prompt, an unclear instruction, a case the format
doesn't handle well), log that as a retro entry too — the recursive
case is high-leverage. The skill should improve from its own output.
