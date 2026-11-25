---
name: commit
description: Author a commit message and commit it — Conventional Commits header, Keep a Changelog body, Source trailer, enforced by a commit-time husky gate if setup (--setup-husky). Use before every `git commit`, whether a human or an agent initiates it, including a run split across commits.
---

Author a commit by running the steps in order. With `--setup-husky`, wire the husky commit-msg hook
into this repository instead, and stop.

## Authoring a commit

Run the steps in order. A split run repeats steps 2 to 6 once per commit.

**1. Read the argument.** It names the staging sets and the commit count —
`/commit stage /folder1 and /folder3 into 2 commits`. A bare `/commit` means you
decide both. An argument overrides a pre-existing index, being the more explicit
of the two signals.
_Done when_ you can state the staging set of every commit you are about to make.

**2. Read the change.** `git status`, `git diff --staged`, `git diff`. A
non-empty index is expressed intent: honour it. An empty index you fill
yourself. Changes outside the staging sets stay uncommitted and get reported,
rather than swept into the last commit. Report unstaged changes either way:
pre-commit verification judges the working tree and not the staged snapshot, so
a half-finished file that is _not_ in this commit can still fail it.
_Done when_ the index holds exactly this commit's set, and you hold the list of
what you left out.

**3. Resolve `Source:`.** Search the prompt, then the conversation context, then
the worktree or branch name — in that order.

| Invocation           | Nothing found                                                 |
| -------------------- | ------------------------------------------------------------- |
| `/commit`            | **Ask.** Nothing in the run says what caused the change.      |
| `/commit <argument>` | **Never ask.** The prompt itself becomes the prose summary.   |
| Agent-initiated      | **Never ask.** The task in flight is the cause; summarise it. |

A hint taken from the worktree or branch name is usable only once **expanded to
a full canonical reference**: `feature/78-commit-skill` yields `78`, which you
expand using this repository's own tracker documentation plus the git remote.
Where mechanical expansion is not possible, drop the hint and keep searching. A
change with no ticket at all is a normal case rather than an error to escalate —
a prose summary of the prompt is a valid value.
_Done when_ you hold a canonical reference, a prose summary, or both.

**4. Author the message, and write it to the draft.** Satisfy the three
conditions below. The draft is `"$(git rev-parse --absolute-git-dir)/COMMIT_DRAFT"`
— inside git's own directory, so it needs no `.gitignore` entry, never reaches
`git status`, and resolves the same from any subdirectory or worktree. Author and
write together, so step 5 never reads a stale draft. A message carrying both
backticks and apostrophes survives no `-m` quoting, which is why it goes in a
file.
_Done when_ the gate exits 0 against the draft. The gate ships with this skill,
at `.agents/skills/commit/scripts/commit-msg` under the repository root, or
`skills/commit/scripts/commit-msg` in a checkout of the skill's own repository.

**5. Commit with `git commit -F <draft>`, letting every hook run.** Step 4's
gate run is fail-fast ergonomics covering only the commits this skill makes, so
the repository's hooks remain the guarantee and `--setup-husky` still earns its
keep. Run no tree verification of your own: a harness repository runs
`verify:commit` at pre-commit, a standalone repository has no such script at
all, and relying on the hooks the repository has is the one rule that holds in
both. That is the entire command — `git commit -F <draft>` and nothing else — so
every hook fires exactly as it would for a human. **Never pass `--no-verify`.**
_Done when_ git reports the commit, or names the condition that failed.

**6. On rejection, repair the named cause and retry the same draft.** A
rejection names a condition, not a wording problem, so fix that condition in
place and re-run the same command. With step 4 already green, a rejection here
comes from a tree check rather than from the message.
_Done when_ the commit exists and
`git log -1 --format='%(trailers:key=Source,valueonly)'` prints a non-empty
value.

**7. Report, and stop.** The commit stays in the local clone: **pushing is the
human's act**, and it is where a local mistake becomes permanent.
_Done when_ every commit made and every change left uncommitted is named in the
report.

There is no approval stop anywhere in this run. The commit is local and
reversible, so `git reset` and `git commit --amend` are the review mechanism,
and the human reviews a real commit with `git show` rather than a proposal.

## The contract — three blocking conditions

The gate is `scripts/commit-msg`. It reads the proposed message and exits 0 or 1.
One message that satisfies all three, end to end:

```text
fix(parser): keep the final trailer block intact

Reading paragraphs eagerly treated the last one as prose, so git returned
nothing for the trailer. The prose explains the why — the diff already
carries the what.

### Fixed

1. The last paragraph is parsed as the trailer block.

### Added

1. A regression test for a message that ends on a trailer.

Source: https://github.com/hancrafted/skills/issues/7 | fix trailer parsing
```

**1. Header.** `type(scope)!?: subject` on line 1, then a blank line 2.

- `type` is one of eleven: `feat`, `fix`, `docs`, `refactor`, `chore`, `style`,
  `test`, `perf`, `build`, `ci`, `revert`.
- `scope` is optional and freeform. Keep changes scoped to one domain.
- `subject` is present tense, and otherwise unconstrained — no length, mood, or
  trailing-period rule.
- `!` is tolerated and carries no meaning.

**2. Body shape.** At least one `### <category>` heading at H3, drawn from Keep a
Changelog v1.1.0's six — `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`,
`Security` — each followed by at least one numbered item (`1. `).

- The set is closed, so headings outside those six are rejected and the body
  stays machine-readable.
- Prose paragraphs are allowed anywhere. Explain the **why** and the **how** —
  the diff already carries the what.
- The gate checks the _shape_ of numbering, never the sequence. Number correctly
  anyway; that is your job, not the gate's.

**3. `Source:` trailer.** At least one non-empty `Source:` **git trailer**, so
every commit's cause is retrievable with one command:

```sh
git log --format='%(trailers:key=Source,valueonly)'
```

- Value is `<canonical ref> | <prompt summary>`. Either part alone is valid;
  carry both when you hold both — links rot, and the summary keeps the cause
  readable after the tracker is gone.
- The canonical reference resolves without context — a full URL for a hosted
  tracker (`https://github.com/hancrafted/skills/issues/2`), a
  repository-relative path for a local one (`docs/specs/0001-commit-gate.md`).
  Where this repository's own tracker documentation states a citation form,
  follow it. A reference that needs the reader to already know the repository —
  `#123`, `78`, `GH-78` — is not canonical; the gate rejects the numeric forms,
  and tracker shorthands like `GH-78` are yours to expand.
- It must be a real trailer, which means the **last paragraph**, preceded by a
  blank line. A `Source:` line placed directly under a numbered item is not a
  trailer, and neither is one followed by another prose paragraph — both look
  fine to a human and return nothing to `git log`.
- Repeats are allowed when a change has more than one cause.

**Provenance is `Source:` alone. Never name yourself as a co-author.** Agent
harnesses append a `Co-Authored-By` for the model by default, and the harness
running you may instruct it outright — strip it either way, along with any
"generated with" line. A human co-author's `Co-Authored-By` is fine; it is part of
the same trailer block. The gate does not check this, because detecting model
names and vendor domains is brittle and stale on every release. It is your job.

Each condition answers to a published finding, and the case against widening the
gate to judge prose is in [`assets/research.md`](assets/research.md). Read it
before changing the contract.

## `--setup-husky`

Run one script and report what it changed:

```sh
sh .agents/skills/commit/scripts/setup-husky
```

It installs husky if absent, writes `.husky/commit-msg` delegating to the gate,
sets `core.commentChar` so the body's `### ` headings survive git's own cleanup,
and is safe to run twice. It aborts with an explanation rather than a raw shell
error when the gate cannot be located — the likeliest cause is an install
performed with `--copy`.

Mechanics, the canonical hook body, the non-Node alternative, and troubleshooting
live in [`assets/setup-husky.md`](assets/setup-husky.md). Consult it when a step
surprises you.

_Done when_ the script reports success, and `.husky/commit-msg` is staged for the
user to commit.

## Installing this skill

```sh
npx skills add hancrafted/skills
```

Project scope — the default — because it is meant to be committed, and that is
what lets the hook run for every clone and in CI. **Never `--copy`**: copy mode
creates independent per-agent copies and destroys the single canonical path the
hook depends on.
