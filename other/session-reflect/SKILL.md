---
name: session-reflect
description: "This skill should be used when the user asks to 'reflect on this session', 'save insights to memory', 'capture what we learned', 'commit this to memory', 'save decisions to Basic Memory', 'write up what we did', 'preserve what we found', 'save insights from this conversation', 'save what was discovered', 'capture session learnings', 'session reflection'. Reviews the current conversation, extracts durable insights (decisions, lessons, gotchas, patterns), previews proposed captures grouped by target note, and writes to Basic Memory after user approval. This captures durable insights as Basic Memory notes — to save URLs or links found this session as Raindrop bookmarks instead, use session-bookmarks."
user-invocable: true
allowed-tools:
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__write_note
  - mcp__basic-memory__edit_note
  - mcp__basic-memory__build_context
  - Skill
---

# Session Reflect

Review the current conversation, extract insights worth persisting in Basic
Memory, find the right existing notes, preview proposed captures, and write
only what the user approves.

User-triggered: extracts candidates, finds the right target notes, shows a
grouped preview, and waits for approval before writing. Thorough by design —
exercises judgment and lets the user decide what's worth keeping.

## Edge Cases

- **Empty conversation / no insights** — report "No durable insights found in
  this conversation" and exit. Do not force captures.
- **BM unavailable** — report the error and suggest trying again later. The
  PostToolUseFailure hook covers BM write-tool errors (write_note, edit_note,
  schema_validate, schema_diff, schema_infer); other tool failures surface raw.
- **All insights already captured** — if `build_context` 1-hop checks show
  every candidate is in a neighbor, report "All insights from this session
  appear to already be captured" with note links.
- **User declines all** — respect the decline. Report "No observations written"
  and exit cleanly.
- **Very long conversation** — cap at 10 candidates in the preview. Note
  "N additional minor insights omitted — request a second pass if needed."
- **Target note has no Observations section** — flag to the user that the
  note needs structural repair. Do not use `operation="append"` with
  `section="Observations"` (it appends to end of file, not end of section).

## Workflow

### 1. Extract candidates

Review the current conversation and identify:
- **Decisions** — architectural or design choices made with rationale
- **Lessons** — things that worked or didn't, confirmed assumptions
- **Gotchas** — surprising behaviors, edge cases, footguns discovered
- **Patterns** — reusable approaches confirmed in practice
- **Limitations** — constraints, known issues, things that can't be done
- **Breaking changes** — API or behavior changes that affect existing code

Be selective — not every exchange is worth persisting. Prefer durable insights
over session-specific context. Skip anything that belongs in project files
(CLAUDE.md, code comments) rather than the cross-project knowledge graph.

### 2. Find target notes

For each candidate insight, search Basic Memory for the most relevant existing
note to append to:

```
search_notes(query="<topic keywords>", page_size=5)
```

Once you have one or two candidate notes, check their immediate graph context
before committing. This surfaces what's already captured nearby and prevents
proposing observations that duplicate content in a linked note:

```
build_context(url="<candidate-note-title>", depth=1, max_related=5)
```

If a neighbor is a better fit for the insight (e.g., the insight belongs to a
more specific linked note), prefer the neighbor over the original candidate.

If multiple notes are plausible targets, pick the most specific one. If no
existing note fits, flag it as a new note candidate (title it generically
enough to be reusable across projects).

Before proposing a new observation, check whether any 1-hop neighbor of the
target note already contains a similar observation. Use the `build_context`
result from above — if a neighbor already captures the same insight, skip the
observation or note "Already captured in \[\[neighbor-note\]\]" in the preview.

### 3. Preview

Before showing the preview, scan each candidate observation for scope-leak
signals. Basic Memory is a cross-project knowledge graph — observations must be
portable across projects. Check for: absolute paths (`/Users/`, `/home/`,
`/var/www`), multi-segment relative file paths with extensions
(`lib/routes/settings.js`), ALL_CAPS env vars 8+ characters not in the
well-known set (`NODE_ENV`, `CI`, `PATH`, `HOME`), and `localhost:` with ports.

Classify each finding:
- **False positive** (path in a generic code example, well-known env var) →
  keep as-is, no change needed
- **Generalizable** → rewrite to use generic descriptions (e.g., "route handler
  file" instead of `lib/routes/settings.js`)
- **Not generalizable** → drop the observation and note in the preview
  ("Dropped: too project-specific")

**Verify before capture.** Separately, scan each candidate for non-trivial
**mechanism or attribution claims** — assertions about _how_ something works,
_what_ caused a behavior, or _who_ authored or originated something. These are
the claims most likely to be confidently wrong and most damaging once persisted
(a wrong note compounds via citation and cross-project reciprocation). For each
such claim, check whether a primary source was actually read this session
(source code, official docs, the changelog, an authoritative API). If not,
either (a) verify it now against a primary source, or (b) mark it in the preview
as **unverified** and weaken it to a hedged form ("appears to", "designed to")
so the user can confirm or downgrade before it is written. Routine observations
(preferences, decisions, recapping what was done) skip this scan.

Show a grouped preview before writing anything:

````markdown
## Proposed Memory Captures

### Appending to: npm-fastify
- [gotcha] The `reply.send()` call does not halt execution — always `return reply.send()` to avoid double-send errors
- [pattern] Use `fastify.register()` with `prefix` option for route namespacing

### Appending to: engineering/agents/basic-memory-note-enrichment-package-metadata-pattern
- [lesson] `edit_note` with `find_replace` is required for mid-section inserts; `append` with `section` goes to end of file

### New note: engineering/agents/session-reflect-patterns
- [decision] On-demand reflection should preview before writing — reduces noise in the knowledge graph

Approve all, or specify numbers to apply individually (e.g. "approve 1,3").
````

Wait for user response before proceeding.

### 4. Write approved captures

After approval, apply each capture (if the preview flagged an observation as
**unverified**, strip that label first — persist only the hedged observation
text, never the literal word "unverified"):

**Appending to existing note** — use `edit_note` with `find_replace` targeting
the last line of the `## Observations` section:
```
edit_note(
  identifier="<note-title>",
  operation="find_replace",
  find_text="- [<last-category>] <last observation text>",
  content="- [<last-category>] <last observation text>\n- [<new-category>] <new observation text>"
)
```

Do NOT use `operation="append"` with `section="Observations"` — it appends to
end of file, not end of section.

If `find_replace` fails (no match found), the note may have been edited since
you last read it. Fall back to `read_note` to fetch current content and retry
with the actual last observation line.

**New note** — use `write_note` with full structure (frontmatter, plus the
`## Observations` and `## Relations` sections). Keep title generic enough to
reuse across projects.

### 5. Relation-count check

After writing, check each target note's outgoing relation count via
`read_note(output_format="json")`. If a note has fewer than 3 outgoing
relations but more than 5 observations, also check incoming links via
`build_context(depth=1)`. Flag sparse notes to the user: "Note X has N
observations but only M outgoing relations — consider adding links."

### 6. Report

Summarize what was written:

````markdown
## Reflection Complete

Saved N observations across M notes:
- npm-fastify — 2 observations added
- engineering/agents/... — 1 observation added
- [new] engineering/agents/session-reflect-patterns — created

Skipped: [anything the user declined and why]
````

## Observation Categories

Use `[decision]`, `[lesson]`, `[gotcha]`, `[pattern]` for the durable core,
plus `[limitation]` and `[breaking]` when scoping constraints or API changes.

| Category | When to use |
|----------|-------------|
| `[decision]` | Architectural or design choice with rationale |
| `[lesson]` | Confirmed or disconfirmed assumption |
| `[gotcha]` | Surprising behavior, edge case, footgun |
| `[pattern]` | Reusable approach confirmed in practice |
| `[limitation]` | Known constraint or thing that can't be done |
| `[breaking]` | API or behavior change affecting existing code |

## Guidelines

- **Preview before writing** — never write without user approval
- **Be selective** — 3 high-quality observations beat 10 mediocre ones
- **Target specificity** — append to the most specific existing note, not a
  catch-all. Create new notes only when no good target exists
- **Keep it cross-project** — avoid session-specific context or project file
  paths. Basic Memory is a cross-project knowledge graph
- **One-liner observations** — each `[category]` line should be self-contained
  and understandable without the conversation context

## Bookmark Delegation

After completing the report (Step 6), invoke `/session-bookmarks` via the
Skill tool to check for bookmark-worthy URLs discovered during this session.
If `/session-bookmarks` finds no candidates, it exits silently.

## vp-beads Integration

In projects using vp-beads, `/session-reflect` and vp-beads workflows are
complementary:

- **Upstream friction** — if research or debugging surfaces a bug or
  limitation in a package or tool, log it via `/upstream-tracker` in addition
  to (or instead of) capturing a `[gotcha]` in Basic Memory.
- **Capture ↔ synthesis** — use `/session-reflect` for in-sprint discoveries;
  at sprint-close, vp-beads' `/retrospective` synthesises those captured notes
  into the sprint record. `/session-reflect` is for durable cross-project
  insights; retrospective is for sprint-scoped synthesis.
