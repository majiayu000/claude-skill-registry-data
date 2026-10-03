---
description: Record why something is the way it is — a decision and its reasoning, a lesson that cost time, or a standing constraint. Use when the reasoning behind a choice would be expensive to reconstruct later.
disable-model-invocation: true
---

# Write down why

The code says what. The git history says when. Neither says **why**, and why is the expensive part
to reconstruct — usually at the moment somebody is about to undo it.

## When to write an entry

Write one when the answer to "why is it like this?" took real work to arrive at, and would take
real work to arrive at again.

Good reasons to write:

- a choice was made between two viable options and the loser is not obvious from the code
- something was tried, failed, and the failure is not visible in the repository
- a constraint exists that a newcomer would break without knowing

Do **not** write an entry when:

- the code already says it — a well-named function does not need a memory entry
- the git history already says it — a good commit message is the right place for "what changed"
- it is a task, not knowledge — that is `STATE.md` or a session record
- it is a procedure — that is `/chamnan:capture`

**This is not a conversation log.** Never paste a transcript. Write the conclusion.

## Pick a category

The three are used differently, which is why they are separate:

| | | |
|---|---|---|
| `decisions/` | A choice and its reasoning | *"Postgres over SQLite — two writers, and SQLite's locking showed up under load."* |
| `lessons/` | Something that cost time once | *"Editing `src/` while the app runs throws an AttributeError. It is a hot-reload artifact, not a bug — restart clears it."* |
| `rules/` | A standing constraint | *"Never add a Cloud fallback for embeddings — a different model means an incompatible vector space."* |

**Rules are injected into every session.** Decisions and lessons contribute their title, and the
agent reads the file when the title looks relevant. So put a constraint in `rules/` only if it
should be in front of the agent before it starts — otherwise it is a decision, and the difference
matters to what every session costs.

## Where it goes

```
.chamnan/memory/<category>/<short-slug>.md
```

A short, specific filename: `postgres-over-sqlite.md`, not `database.md`. The filename is what
appears in the session listing beside the title, so it should be recognisable on its own.

**Check the directory before you write, and treat a name that differs only by case as taken.**
macOS and Windows have case-insensitive filesystems by default, so writing `No-Force-Push.md` where
`no-force-push.md` already exists does not create a second file — it leaves one file carrying the
first name and the second entry's content, with nothing on disk recording that anything was lost.
`git status` shows it as an ordinary edit, so there is no second chance to notice. If the name is
taken in any casing, either update that entry or choose a different slug.

## The format

```markdown
# One line saying what this is about

<Two or three sentences. What was decided or learned, and why.>
```

No frontmatter. The first `# ` line is the title; everything else is prose. Keep an entry short —
if it needs headings and subsections, it is documentation and belongs in `docs/`.

Write the reasoning, not just the conclusion. *"We use Postgres"* is worth nothing in six months;
*"Postgres, because two processes write concurrently and SQLite's locking failed under load"* is
worth the file.

### Decisions: name what you rejected

A decision entry gets one more line, as its own field rather than a sentence buried in the prose:

```markdown
# Postgres over SQLite

Two processes write concurrently, and SQLite's locking failed under load.

**Rejected:** SQLite — simpler to run, but the locking behaviour above ruled it out.
```

**`**Rejected:**` as a heading, not a sentence you might skip.** This is usually the more valuable
half of the entry: six months from now, someone re-proposing the rejected option is the exact
situation this file exists to prevent, and a sentence buried in prose is easy to skip past under
deadline while writing quickly. Leave it out only when there genuinely was no real alternative
being weighed — not when there was one and it felt obvious at the time; obvious-at-the-time is
exactly what stops being obvious later. `chamnan-report` counts decisions with nothing here, so a
gap is visible rather than silent.

### Give a rule a `**Check:**` when it can have one

A rule that is only prose is statistically hard to tell apart from no rule at all. If the rule can
be checked mechanically, add one line and it is verified every session instead of read and forgotten:

```
**Check:** present `PATTERN` in `GLOB`
**Check:** absent `PATTERN` in `GLOB`
**Check:** present `PATTERN` in every `GLOB`
```

**Say `every` whenever the rule means "each one".** Without it the check is aggregate across the
whole glob — `present X in config/*.yaml` is upheld while ANY one file matches, so adding a config
that violates the rule still reports `holds`. That is the trap; `every` is how you avoid it, and it
names the offending file when it breaks.

### `As-of:` and `Provenance:` are not yours to write

A hook adds these automatically the first time a file under `.chamnan/memory/` is written or
edited — `**As-of:** <today's date>` and `**Provenance:** ai-drafted`. Do not add them yourself;
if they are already there, leave them alone. `Provenance` moves to `ai-confirmed` only when a
human reviews and keeps the entry, which is a later, separate step — not something this skill
does.

## What not to put in it

- **No credentials, tokens, hostnames or connection strings.** These files are committed. The
  session-start hook redacts what it injects, but that does not clean the file on disk.
- No pasted conversation, no logs, no stack traces. Name the error; do not paste the session.
- Nothing that expires. An entry that will be wrong next month is a note, not a memory.

## Housekeeping

Memory is **not** pruned by age. A session record stops mattering; a decision does not, and
deleting on a timer would throw away the oldest entries, which are usually the ones nobody can
reconstruct.

Growth is bounded where it costs something instead — at the injection. Rules are capped by length
and the title list by count, so a repository with forty entries costs the same per session as one
with four.

Entries are ordinary markdown. Edit them when they change; delete them when they stop being true.
A memory nobody prunes by hand eventually contains something false, and a false entry is worse than
a missing one. Set `"memory": false` in `.chamnan/config.json` to switch the whole thing off.

## Name the thing, do not describe it

A recorded decision is read months later, often by a session that has just been compacted. What a
compaction destroys first is identifiers: summarization recovers roughly **63% of facts**, and the
measured failure mode is paraphrase — `src/middleware/auth.ts:52` returning as "the auth middleware
file". The sentence survives; the ability to find the file does not.

Write the path, the symbol, the command, the commit, the number. `mapper.py:566` and
`source.count("\n") + 1` are greppable a year from now. "the line-count bug" is not.
