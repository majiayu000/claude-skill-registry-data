---
name: commits
description: >-
  v1.1.15 — Give each complete capability sentence its own Feature and working
  commit. Every separate "It should also" sentence gets a new ledger row;
  an optional "and may" clause inside one sentence stays in that row.
---

# Feature commits

Apply this skill at each source write, not only when reviewing finished history.
When workflow is selected, its `Write code` phase contains the entire Feature
queue; a small program, one module, or a focused repair does not combine
separate sentences.

Before each implementation edit, read the first uncommitted ledger row from
the original request and state its exact sentence, planned conventional commit
subject, commands allowed now, and commands deferred to later rows. Compare
that allowed set with the original sentence, not a previous summary of the
program. Write only the current row's implementation, then verify and commit
it before writing the next row. This also applies to the first file creation.

Before writing code, extract the capability sentences from the original
request before grouping commands or choosing a commit count. Copy one complete
sentence per numbered row; a row containing a period followed by another
"It should also" capability must be split before any implementation. Related
behavior cannot remove that sentence boundary.
**Copy each complete capability sentence verbatim into its own row**, then
read it back against the source request character by character before code:
copy the complete capability sentence rather than retyping it from memory.
If explanatory/setup sentences share its source line, leave them outside the
quoted capability. A row that quotes context plus the repair sentence is not
the requested verbatim capability sentence. Preserve
inline backticks around terms such as `ValueError`, the closing parenthesis,
any "and may" clause, and the final period; a nearly identical paraphrase is
not a verbatim ledger sentence. Then list that row's commands, required
behavior, and planned conventional commit subject. Setup text naming only an
artifact, signature, or skill is not a Feature. Never create a ledger row
for a public function signature or duplicate an existing capability sentence
to match a guessed count. A duplicate sentence cannot be a later Feature.
Count the source sentences,
not commands or a preferred number of commits. Match every capability
sentence to exactly one row and every row to exactly one sentence before
editing; abbreviated quotes, merged sentences, and duplicate rows quoting
the same sentence are invalid.
An optional clause is not a complete sentence on its own. Before the first
implementation edit, check that no row starts with an extracted "and may"
clause and that no earlier row stops before that clause or its final period.
If either occurs, restore the whole source sentence in one row now. A later
optional-command commit belongs beside that same row; a new row for it fails
the ledger even when its implementation is a valid focused follow-up.

Cross-check each row's command list against its own quoted sentence. Commands
named only in a later source sentence stay deferred to that later row; do not
attach them to the current row merely because they are convenient to implement
together. A missing row must be restored before writing its commands, not
folded into an earlier Feature.


Each later "It should also …" sentence starts a new row, even when related
to the preceding sentence. Commands and optional "and may" clauses before
the same sentence's final period remain in that row; do not split them into
another Feature. A comma does not end a sentence or create a new Feature.
Sentence boundaries apply whether capabilities occupy separate lines or share
one paragraph or line. Related commands in separate sentences still need
separate rows; commands within one sentence stay together. Keep dependency
order where possible, without changing these boundaries.
Before the first source edit, scan the ledger for a row that contains a
second complete capability sentence, especially another "It should also".
If one exists, stop and split that row. Do not call the whole paragraph or
the whole program one Feature.

Keep the original ledger visible and preserve its boundaries through the whole
task. Record the verified commit beside the active row before advancing. After
a merge or verification step, resume the first uncommitted original row; do not
replace the remaining rows with a new combined summary. A shared dispatcher must expose only capabilities
implemented so far, even when adding all remaining cases seems easy.

The first source file you write is already an implementation edit: it may
implement only ledger row 1. Do not draft the complete multi-Feature program in
one file write and plan to separate it with later commits. Before each new
Feature commit, inspect the full source tree you are about to commit, not just
the diff: if the public entrypoint can already execute a later row's capability,
remove that capability from this edit and implement it after this commit.
Recount the original capability sentences against ledger rows before this
first write and before each commit; a count mismatch means the current
Feature is not ready to implement or commit.
If the first source draft already dispatches every command, reduce it to row 1
before committing; later commits that add duplicate handlers do not repair an
early bundle. At handoff, compare the number of distinct introducing Feature
commits with the ledger entries and inspect the first Feature's committed tree.

## Complete and commit the current entry before starting the next

Treat the ledger as a queue. Work on only its first uncommitted entry:

- Implement its commands, helpers, validation, and required output. Preserve
  earlier Features; keep the program working at every commit.
- Preserve the requested output and public API. Judge completion by what the
  implementation does; labels may be assembled at runtime when appropriate.
- The staged implementation contains earlier Features plus the current Feature,
  with no later capability implemented in advance. Shared helpers needed now
  are fine. Check the executable behavior and diff against the next ledger
  entry before committing; descriptions of future work are not implementation.
- Include that Feature's applicable tests, logging, comments, and documentation
  in its commit. Do not postpone those obligations into planned cleanup commits.

Close each entry with this gate:

1. Compare the diff with the active row and every pending row: any later row's
   command handler or working capability means this change is not ready to
   commit. If the proposed commit subject or staged source names a capability
   from the next source sentence, split the change before committing, even
   when both capabilities live in one file. Defer that implementation before
   staging. Verify the current behavior
   and rerun a representative public-entrypoint example for every earlier
   Feature, especially after changing parsing or dispatch. Resolve failures
   before staging.
2. Stage only its changes in the worktree.
3. Use the current row's planned subject: `feat: <current capability>` or
   another applicable conventional type; a plain `Add ...` or `Fix ...`
   subject is invalid.
   Run `git commit` as its own command, not chained behind a search or check
   that could fail and silently skip the commit. The Feature commit subject
   uses a conventional-commit type (`feat`, `fix`, `refactor`, `chore`,
   `docs`, `style`, `test`, `perf`) in `type:` or `type(scope):` form. A
   subject that omits that type is not a completed Feature commit.
4. Read the new `HEAD`, confirm it advanced and contains this entry's Python
   implementation, and record that commit beside the ledger entry. Its
   introducing hash must differ from every earlier row's introducing hash;
   assigning one hash to several rows exposes bundled implementation, not
   completed entries. Inspect that commit's full source to confirm no later
   row already works, even if a later commit claims to add it. If the
   commit failed, resolve it and commit before editing the next Feature. If
   the first file was written outside the intended worktree, move that work
   into the worktree and complete the first Feature commit before advancing.

A statement that a Feature is tested or complete is not a commit. Only an
entry with a verified commit may be removed from the queue.

## Verify delivery against the ledger

Each entry must map to a distinct commit in order; inspect what each mapped
commit actually introduced, not just its subject or the total commit count.
The mapped Feature commit subject must still use a conventional-commit type
in `type:` / `type(scope):` form.
A later Feature must not already exist in an earlier Feature's Python tree.
Do not batch missing entries into one final commit or split already-written
Features into cosmetic commits after the fact.

If a defect is discovered after a Feature was committed, commit a focused repair
before adding the next Feature. Verify the repaired tree preserves all earlier
Features. The original Feature commit plus its immediate repair is a valid
completed entry; a repair cannot rescue bundled Features. Optional extras may
land in a focused follow-up before advancing to the next entry. Record that
follow-up beside the same original sentence, never as an extra ledger row.
Compare the saved ledger against the original request, including punctuation,
rather than reconstructing sentences from command names. Never rewrite
history to repair a commit.

A request with only one complete capability sentence needs one Feature commit.
"Undivided change" never overrides the source-sentence boundaries: a task with
separate capability sentences is not one Feature because it describes a tiny
program, one file, or one public entrypoint. Its ledger and separate introducing
commits remain required. Commits happen in the worktree; worktree location and
merge policy belong to the applicable project instructions.
