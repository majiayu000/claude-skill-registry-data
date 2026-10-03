---
name: crav1-code-into-specs
description: >-
  Sort a code change that already landed onto specs that already exist.
  The change is a commit, a commit range, or the current branch diff.
  No dump is required. Quote what the change does into the matching
  spec.md files, then report whether docs/system/ or another spec has
  to change. Does not create a slug. Does not watch the repo.
  Does not seed docs/system/. When that folder exists and glossary.md is
  missing, fills only that file from the landed change. When the file exists,
  appends only words that are not already rows. Does not rewrite existing
  glossary rows. A meaning the change does not state is `to be researched`.
  Does not write application code. Does not plan, implement, or commit.
disable-model-invocation: true
icon: file-diff
color: teal
---

# Code into specs

You sort a code change that already landed onto specs that already exist. Then you write what belongs into the matching `spec.md` files, the same way `/crav1-add-to-spec` writes a quote. Then you check whether `docs/system/` or another spec has to change, and you report that impact. You do not silently rewrite those other files. You do not write application code. You do not plan, implement, or commit.

This is not a mode of `/crav1-match-to-specs`, `/crav1-match-dump-to-specs`, or `/crav1-add-to-spec`. Match creates spec folders from repos plus a dump. Match-dump sorts a later dump onto specs that already exist. Add takes information already aimed at one named spec. This skill starts from a code change that already landed without spec, plan, or build. No dump is required. Do not send this job to those commands, and do not absorb theirs.

Do not copy the match worker that creates folders. Do not use `crav1-match-to-specs` `references/slice.md`. Do not launch a worker. There is no slice subagent.

This skill does not watch the repo. It runs only when someone points it at a change. Do not schedule it, hook it, or run it again because new commits appeared.

This is not `/crav1-tighten-spec`. Tighten is for mushy wording. This skill is for a change that already landed. If the message is only “make this tighter” and brings no change, tell them `/crav1-tighten-spec` and do not edit.

This is not `/crav1-intake-to-specs`, `/crav1-spark-to-spec`, or `/crav1-ideas-to-spec`. Those create the folders. Do not create a slug here. Do not invent a landscape from the diff alone.

A not-started spec (match status `not in the code`, or a thin spec) can keep taking information until planning. Adding what the change does does not start planning and does not write `plan.md` or `tasks.md`.

## Input

Everything after `/crav1-code-into-specs`, and every `@`, is the pointer: a commit, a commit range, or the diff of the current branch against the default branch, when they named one. No dump is required. Do not ask for notes, tickets, or a dump.

Do not ask for a slug first. An `@` of one spec folder is a hint for the sort, not a requirement. It does not limit the sort to that folder, and it does not replace the change.

## Specs (no sort yet)

Spec folders are `docs/specs/<slug>/` with a `spec.md`. Skip `_template`.

Read those folders before you sort. Do not ask which slug.

If there are no spec folders, stop. Point at `/crav1-match-to-specs`. Do not invent a landscape from the diff alone. Do not create a slug. Do not seed `docs/system/`.

## Change (no sort yet)

The change is one of these, when they named it:

- a commit (a hash they already gave, `HEAD`, or a subject that matches one commit)
- a commit range (`A..B`, `A...B`, or from one commit to another)
- the diff of the current branch against the default branch (they said this branch, the branch, or the branch diff)

If they named one, that is the change. A named range is one change. Do not ask. Do not ask them to type a hash. Do not split one change into several runs.

If they did not name one, look at git, then ask with options only. Use the questions tool when it is available. Do not guess a change and start sorting. Do not ask them to type a hash.

- Default branch: the branch `origin/HEAD` points at, or `main` when that is the default you can see.
- Recent commits: a short list from `git log` on the current branch. Each option is that subject. A short hash may sit beside the subject so two subjects can be told apart. The choice is the option.
- Branch diff: one option, the diff of the current branch against the default branch (commits on this branch that are not on the default branch, as one change). If that diff is empty, do not offer it. Say the branch diff is empty.

Stop until they pick, when a pick is required. The pick is the change.

## Sort (no writes yet)

Read every existing `spec.md` (skip `_template`) and the change (its diff and its commit messages). Then show three piles. Do not write files.

1. **Belongs to this spec** — the change does something that spec does not already say. Name `docs/specs/<slug>/` and the heading the words would go under. Quote what the change does.
2. **Already described there** — that spec already says what the change does. Name the slug and the heading. Do not plan a second copy.
3. **Fits none of them** — what the change does that matches no existing spec. Leave it on the list. Do not invent a slug.

A named slug in the message is evidence. It does not skip the other piles. Something with no slug is sorted by what the change does.

Split a fact that is partly new and partly already described. One fact is in one pile.

Put every fact you will treat as accepted on the sort. A fact you leave off stays inferred.

Stop. They confirm or edit the sort. Do not write files. That confirmation is the only stop before writes. Do not ask for a slug. Do not open a mushy interview, an architecture interview, or an export-format question. If they edit the sort, the edit is the confirmation. Do not ask again. Use their slugs and piles. A fact they struck, or that you never put on the sort, stays labeled inferred if it appears later. Confirming the sort confirms the facts they left on it.

## Write what belongs

Edit only `docs/specs/<slug>/spec.md` for slugs in the confirmed **belongs** pile. Write them in this chat. Do not launch a worker.

For each of those files, write the same way `/crav1-add-to-spec` writes:

- Quote what the change does. The quote is the record. Do not replace it with a paraphrase. A reading you add that the change does not show is inferred or it stays out.
- Label what is new versus what was already there.
- Keep inferred facts labeled inferred. A fact you were not shown by the change, and that the file did not already say, is inferred or it stays out. A fact that was not on the confirmed sort stays inferred or stays out.
- Do not invent acceptance, architecture, or tasks to fill gaps. A proposed ADR or diagram edit later is only a change the diff requires.
- Do not change match status unless the change itself says the status changed.
- Do not write `plan.md`, `tasks.md`, `diagrams.md`, `adr/`, `export/`, `verify.md`, `fix-log.md`, or `work-item.md` in the spec folder.
- Do not replace the file with a template.

Labels, in the section the words belong to:

- `**New:** "…"` — what the change does, added this pass.
- `**Already there:**` — do not paste a second copy. Leave the existing sentence. The **already described there** pile is the report, not a second paste.
- `**Inferred:**` — a connection you drew. Not an accepted fact.

When the file already has `## Trace`, append one line: what this pass marked new, already there, and inferred. Do not create `## Trace` only for that line.

A thin spec (match status `not in the code`, or only Match / What the dump says / In the code / Trace / Open questions) stays thin. Put the quote under the heading it belongs to. Add a heading only when the change is that content. Do not add Problem, Goals, Users and journeys, or Acceptance criteria to fill the file out. Do not add `## In the code` unless the change names code that is there.

A fuller spec keeps its headings. Place the quote in the section it extends. Add an acceptance checkbox only when the change states a check a stranger could run, and label that checkbox `**New:**`. Do not turn a behavior into a checkbox the change did not state.

Expected headings when the file already uses the full spec shape: this skill’s `assets/spec.md` (same file as `docs/specs/_template/spec.md`; drop-in: `.cursor/skills/crav1/crav1-code-into-specs/assets/spec.md`; plugin: this skill’s `assets/spec.md`). A match-shaped spec does not have to grow those headings.

The **fits none of them** pile is listed and left alone. Do not create a spec for it. If they say to create one, do not write a folder here. Point at the skill that creates a spec, and do not run it:

- one or two sentences for one feature: `/crav1-spark-to-spec`
- one unstructured pile for one feature: `/crav1-ideas-to-spec`
- several new features, or several repos: `/crav1-intake-to-specs`
- repos that already make up the system, and this leftover is a slice to match: `/crav1-match-to-specs`

## Impact (before any other edit)

The new quotes are already in the matching specs. Read `docs/system/` when it exists (`landscape.md`, `repos.md`, `diagrams.md`, `glossary.md`, `adr/`) and every other `docs/specs/<slug>/spec.md` (skip `_template`). Other means a spec that did not just receive a new quote, plus any heading on a spec you did edit that the confirmed sort did not already cover. Check whether what the change does contradicts or extends the landscape, a repo row, a diagram, an ADR, or another spec.

Section names for that read, not a file to paste over what exists: this skill’s `assets/system/` (same files as `docs/system/_template/`, including `glossary.md`; drop-in: `.cursor/skills/crav1/crav1-code-into-specs/assets/system/`; plugin: this skill’s `assets/system/`).

Do not edit anything outside the confirmed belongs writes in this step, except the glossary gap below. Do not seed `docs/system/` when it is missing. Say it is missing and that this command does not create it. Do not invent a landscape from the diff alone. When that folder is missing, do nothing about a glossary.

**Glossary.** When `docs/system/` is missing, do nothing about a glossary. When it exists and `glossary.md` is missing, write only that file from `assets/system/glossary.md`. When `glossary.md` already exists, append only words or abbreviations the change uses that are not already rows. Do not rewrite, reorder, or edit existing rows. Do not change a Meaning cell that already has text. Source is the landed change. Do not invent terms, expansions, or definitions. Do not write TBD or to be decided. A row is only a word or abbreviation that change already uses. When that same change already says the expansion or meaning, put that text in Meaning. When the change never says what it means, set Meaning to `to be researched`. Skip ordinary English. A code identifier is not a row unless the change already treats that word as a term. Write the file even when it has no rows. This write is not an apply option, and it does not rewrite any other landscape file. Do not list a rewrite of existing rows.

Do not edit `plan.md` or `tasks.md` when they exist, and do not list them as proposed edits. One line in the report when they exist: they were left alone. Adding what the change does does not start planning.

Report:

- If nothing else is affected, say so. Do not ask. `docs/system/` and the specs outside those writes stay as they are.
- If something else is affected, stop and ask. Options only. Use the questions tool when it is available.
  1. **Apply the listed edits**
  2. **Leave the other files alone**
- List each proposed edit in one line: the file, and what would change. One line per file change. No surrounding rewrite.

Do not silently rewrite `docs/system/` or specs the sort did not already write. The glossary write above is the exception: a missing file, or new rows appended to an existing file. Apply the other edits only if they pick apply, and only the lines you listed. If they pick leave, do not edit those files. Do not rewrite existing glossary rows either way.

## Stop

Do not plan. Do not implement. Do not commit. Do not run `/crav1-finalize-commit` or `/crav1-plan-from-spec`. Do not watch the repo.

Output only:

- The change (which commit, range, or branch diff)
- Each `docs/specs/<slug>/spec.md` that gained a new quote
- What was added (what the change does, labeled new) and what was already described there
- The fits-none list, left alone. If they asked for a new spec, which existing skill you pointed at
- `glossary.md` when this turn created it or appended rows. If `docs/system/` was missing, say no glossary was written. If no new rows were appended, say so
- Impact: nothing else, or the one-line edit list and which option they picked
- Next: `/crav1-finalize-commit` only if any file changed and they want those spec edits committed (no push). `/crav1-plan-from-spec` only for a slice they choose. Do not run either.

## Style

Be concise. Quote what the change does. Prefer the smaller edit. Do not invent content to fill gaps. A missing `glossary.md` is written only when `docs/system/` already exists. New rows are appended to an existing glossary. Existing rows are not rewritten.
