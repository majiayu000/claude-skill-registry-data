---
name: knowledge-maintain
description: "This skill should be used when the user asks to fix, repair, or tidy one or more SPECIFIC named notes — 'fix these notes', 'fix the issues in [note]', 'add the missing relations to [note]', 'tidy up [note]', 'fix orphan [note]', 'apply the gardener findings for [note]'. Applies structural fixes (missing sections, relation-verb drift, frontmatter case) directly and inline, and confirms content-level changes (prose rewrites, merges, archival) with the user before applying them. NOT for read-only auditing (use /knowledge-garden), NOT for creating new notes (use /intel), and NOT for graph-wide or autonomous remediation ('fix the whole audit', 'remediate the graph', research-and-document sweeps) — those belong to the knowledge-maintainer agent, which this skill delegates to when invoked broadly."
user-invocable: true
disable-model-invocation: true
argument-hint: "[note ...]"
allowed-tools:
  - mcp__basic-memory__search_notes
  - mcp__basic-memory__read_note
  - mcp__basic-memory__edit_note
  - mcp__basic-memory__move_note
  - mcp__basic-memory__schema_validate
  - mcp__basic-memory__build_context
  - mcp__basic-memory__list_directory
  - Agent
---

# Knowledge Maintain

Apply targeted fixes to Basic Memory notes — missing sections, relations,
structural tidies, archival — with the user confirming changes inline. This is
the scoped, interactive sibling of the `knowledge-maintainer` agent: it owns the
common case (repair a few named notes, where being in the main session means the
user sees each edit) and delegates heavy, autonomous remediation to the agent.

**Write discipline (non-negotiable):**
- `edit_note` with `find_replace` ONLY. Never `append` with `section=` — it
  appends to end-of-**file**, not end-of-section, the documented BM footgun.
- `write_note` and `delete_note` are intentionally excluded. Create new notes
  via `/intel`; archive via `move_note` to `archive/`.
- Read the live note before every edit (verify-before-fix). A flagged issue may
  be a parse artifact, or the note may already be correct.
- One `edit_note` per note per message — issue same-note edits sequentially and
  re-read before re-anchoring after any lands (concurrent same-note edits are a
  precautionary hazard; see `intel`'s `note-write-mechanics.md` single-writer rule).
- `schema_validate` after every edit. If its output appears to repeat the same
  value, trust the note body (`read_note` JSON) as the source of truth rather
  than inferring a duplication from the validator response alone.

## 1. Decide venue (scoped inline vs delegate)

Classify the request first:

**Delegate to the agent** when the work is heavy or autonomous — any of:
- "Fix the whole audit", "remediate the graph", "fix everything".
- The fix requires creating notes or running research: "research and document
  missing packages", anything that would spawn `/intel`.
- Brew-note refresh batches, graph-wide orphan linking, or any sweep across a
  whole ecosystem/type.

To delegate, launch the write agent and stop: call
`Agent(subagent_type="knowledge-maintainer", description="Graph remediation from audit", prompt="<the user's original request, verbatim; include the gardener report if one is in context>")`
— i.e. pass a `description` of "Graph remediation from audit" and a `prompt`
that is the user's original request verbatim, including the gardener report
if one is already in context.

**If the `Agent` call fails or returns no usable report** (unknown subagent type,
error payload, or empty output — the `knowledge-maintainer` agent may not be
installed), say so explicitly and state clearly that **no edits were applied** —
do not fabricate a remediation summary or let the user assume fixes happened.
Offer to apply a named scoped subset inline as a fallback.

**Run inline (scoped)** when the request names a bounded set of notes and a
clear set of findings (roughly 1–8 notes). Proceed to step 2. If scope grows
mid-task (e.g. a "fix this note" turns into needing a new note), stop and
recommend the agent or the relevant intel skill rather than expanding inline.

## 2. Resolve and load each target

For each named target, resolve it to a canonical note before reading:

- Plain title (e.g. `npm-umzeption`) → confirm it exists with
  `read_note` directly; if not found, fall back to `search_notes`.
- Prefixed identifier (`brew:ripgrep`) → map the prefix to its directory and
  locate via `list_directory(dir_name="<dir>", file_name_glob="*<name>*")`.
- Topic phrase → `search_notes(query="<phrase>", page_size=10)`, take the
  matching cluster, and present the candidates as the notes to fix (if the
  match is ambiguous, confirm with the user before editing anything).

Prefix-to-directory mapping (same table `/knowledge-garden` uses):
`npm:`→`npm/`, `crate:`→`crates/`, `go:`→`go/`, `composer:`→`composer/`,
`pypi:`→`pypi/`, `gem:`→`gems/`, `brew:`→`brew/`, `cask:`→`casks/`,
`action:`→`actions/`, `docker:`→`docker/`, `vscode:`→`vscode/`, `gh:`→`gh/`,
`plugin:`→`plugins/`, `skill:`→`plugins/`, `git:`→`engineering/git/`
(git_builtin notes are conventionally plain-titled like `git-replay` and also
resolve via the plain-title path above).

Exclude schema notes (permalinks under `/schema/`) — they are structural
definitions, not subject content.

Once each target resolves, read the live content as the source of truth:

```
read_note(identifier="<permalink-or-title>", output_format="json")
```

Confirm the finding still holds against the actual note. If the premise is
wrong (the section already exists, the "duplicate" is a stub, the note already
ships correctly), STOP and report what was found instead of editing. Derive the
exact surrounding text for `find_replace` from what was read — never assume
whitespace or line counts from a third-party report.

## 3. Classify each fix: auto vs confirm

| Auto-fix (apply directly) | Confirm first (content-level) |
|---------------------------|-------------------------------|
| Missing `## Observations` / `## Relations` heading | Merging duplicate notes |
| Observation section trailing after `## Relations` | Rewriting prose / observations |
| Relation verb drift (`related_to`→`relates_to`) | Archiving a note (`move_note`) |
| Adding a genuine missing `[[wiki-link]]` relation | Changing a note's meaning or scope |
| Frontmatter type case / snake_case fixes | Anything destructive or hard to reverse |

For confirm-first changes, present the exact before/after and wait for the
user's response before executing.

When a fix could plausibly fall in either column — especially any edit that
alters observation *wording* rather than purely relocating it — default to
confirm-first. The auto-fix column is a positive list; treat anything not
clearly in it as confirm-first.

## 4. Apply the fix

Use `edit_note(operation="find_replace")` with text anchored on content read in
step 2. Typical patterns:

- **Move trailing observations into `## Observations`** — two `find_replace`s in
  strict order: **(1) insert first** — anchor on the first `## Relations` line and
  prepend the observation lines before it; if this no-matches, STOP (original
  content is untouched), report, and ask how to proceed. **(2) strip second** —
  only after a re-read confirms the lines now appear in `## Observations`, strip
  the stray trailing heading and its now-duplicated lines. Never strip-before-
  insert: that leaves the note content-less if the insert no-matches.
- **Add a relation** — before appending, verify the target exists with
  `read_note(identifier="<exact-target-title-or-permalink>")`; if not found,
  fall back to `search_notes(query="<target-title>")` for a closer match.
  `read_note` is an exact-match lookup and is the only correct primitive for
  this binary exists/doesn't-exist gate — `build_context` does fuzzy/related
  resolution (it can return an unrelated note that merely *mentions* the
  target phrase in its own prose as a "related" hit) and must never be used
  to decide whether a target exists. `build_context` is only appropriate
  *after* existence is confirmed via `read_note`, to surface additional
  related/inbound context. If `read_note` resolves the target directly,
  anchor on the last existing relation line and append the new
  `relates_to [[target]]` line after it. If only the `search_notes` fallback
  finds a candidate, that is a **fuzzy match, not a resolved target** —
  mirror step 2's Topic-phrase rule and confirm the exact title with the user
  before appending anything; never auto-write a relation to a fuzzy match.
  If neither `read_note` nor `search_notes` finds anything, do NOT add the
  relation — report it as an unresolvable target in step 5 instead of
  silently dropping or silently adding it.
- **Fix a verb** — find the exact malformed line, replace with the canonical verb.

Preserve meaning exactly — moves and verb fixes are not rewrites. When dropping
a heading would lose date/provenance context, fold a brief inline marker (e.g.
`(Sprint 20)`) onto the moved lines rather than discarding it. For any multi-step
fix (especially the insert-then-strip move), proceed to step 5's count assertion
before considering the note done.

## 5. Validate and report

After each note's edits, run `schema_validate(identifier="<note>")` (validate
the single edited note via `identifier`, not the whole `note_type` batch).

**Confirm content survived, not just that it validates.** For any multi-step
edit (e.g. the insert-then-strip move): record `N_before` = observation count
from the step-2 JSON read, then after all `find_replace`s re-read via
`read_note(output_format="json")` and compare `N_after`. `schema_validate`
passing with `N_after < N_before` is the exact data-loss signature — a note that
silently lost observations still validates cleanly. `N_after == N_before` (or
higher, if observations were intentionally added) is the passing gate. If a
multi-step edit landed only partially, the note is in a damaged/partial state:
report it explicitly and restore the removed content before continuing.

**If `error_count` is not 0**, do NOT report the fix as complete. Determine
whether your edit caused it or merely revealed a pre-existing issue (the
`edit_note` re-parse gotcha), surface the exact errors, state that the note is
currently schema-invalid, and either correct it or flag it prominently — never
close out a maintain pass with an unresolved non-zero error count framed as
success.

Then report per note:
- The before/after of what changed.
- The `find_replace` operations run.
- The post-edit validation result.
- Anything left out of scope (e.g. a schema question deferred to
  `/schema-evolve`, a content change the user declined, or a relation whose
  target didn't resolve via `read_note`/`search_notes`).

## Edge Cases

- **Unresolvable relation target** — a proposed `relates_to [[target]]` whose
  target doesn't resolve via `read_note`/`search_notes` is never added and
  never silently dropped: report it as an unresolvable target and suggest
  `/intel` if it looks like an undocumented
  package/tool, or ask the user to confirm the correct title.
- **`edit_note` re-parse gotcha** — `edit_note` re-parses the ENTIRE note after
  a raw string replacement, so a pre-existing unrelated issue can trip on your
  edit. Report it; do not expand scope to fix unrelated problems.
- **Duplicate-frontmatter trap** — never let a `find_replace` cross a `---`
  frontmatter boundary on a schema note; it can create a duplicate frontmatter
  block. Keep find/replace inside the body or inside the YAML block, never
  spanning the markers.
- **No-match on find_replace** — re-read the note, adjust the anchor once, then
  report to the user if it still fails. Do not loop.
- **Schema-level finding** — unmatched observation categories across a type are
  a `/schema-evolve` question, not a note edit. Leave the note untouched.
- **BM write error** — the PostToolUseFailure hook classifies `edit_note`/
  `move_note` errors and emits recovery guidance; follow it.
- **Mid-batch failure** — if a write fails for one note in a multi-note pass,
  stop that note's fix sequence, continue the rest, and report which notes were
  fully fixed, which were partial, and which were not reached. Never summarize a
  truncated batch as complete.

## Guidelines

- **Venue first** — classify scoped vs heavy before touching anything.
- **Verify before fixing** — read the live note; confirm the premise.
- **`find_replace` only** — never `append`+`section`.
- **Confirm content changes** — auto-fix structure; ask before prose/merge/archive.
- **Validate after every edit** — `schema_validate`, expect 0 errors.
- **Stay in lane** — no new notes (use intel skills), no deletes (use `move_note`
  to `archive/`), no graph-wide sweeps (delegate to the agent).
