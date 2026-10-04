---
name: open-pr
description: Open pull requests in a consistent format. Use when opening or updating a PR, or when follow-up commits leave an open PR's title or body stale.
argument-hint: "[--[no-]capture] [--[no-]annotate]"
---

## Process

### 1. Establish the state

Check the working tree, the current branch, and whether the branch already has an open PR: the three facts that decide whether you branch, open, or update in place.

When a PR already exists and you're here because follow-up work landed rather than because the user asked, refresh only when the new commits make the title or body stale — scope, approach, or context they no longer explain.

Uncommitted changes are part of the work: commit them per `/commit`, in every state, before composing. Done when the work sits committed on a non-default branch and you know the base branch and whether a PR exists.

### 2. Read the branch

Study the branch as a whole — `git diff <base>...HEAD` and `git log <base>..HEAD` — for what changed, why, and what a user sees differently. Done when every commit on the branch is accounted for in your understanding.

### 3. Compose

Load `/humanize` first: every word of the title, the description, and the comments follows it.

Compose the title and description fresh from the branch you just read — whether the PR is new or already open — per the formats below. If the repo ships a PR template (e.g. `.github/pull_request_template.md`), its structure wins — apply the section guidance here within the template's sections.

When updating an existing PR, human-supplied material survives: carry over Evidence content and To-do items (including checkbox state), merging in new ones.

Draft the inline comments here too: they come from the same reading of the branch as the description.

Two questions then go to the user in one `AskUserQuestion` call, each asked only when it's live:

- **Evidence** — when the Overview describes something a user sees and the session holds no captures: capture evidence now, take a file the user points at, or skip.
- **Annotation** — when you drafted comments: post them with the PR, or leave the diff clean. Name what they'd say.

`--capture` and `--annotate` settle these two in advance, and their `--no-` forms settle them the other way. A flag skips the question, not the judgement: with nothing worth capturing or nothing that earns a comment, you produce neither.

Capture before the PR exists so it lands complete; when capture fails, carry on without it.

Done when a title and every live section are drafted, any evidence sits on disk, and you know which comments (if any) to post.

### 4. Create or update

Push the branch, then create the PR or edit the existing one, attaching Evidence per `/attach-media`. Mark the PR draft when work you know about still blocks review — otherwise ready; ask only if genuinely unsure. Done when the PR exists and you've reported its URL.

### 5. Annotate the diff

Post the comments you drafted, if any, as one batched review. `gh pr review` has no inline support, so it's `gh api repos/<owner>/<repo>/pulls/<number>/reviews` with `event: COMMENT` and a `comments[]` array of `{path, line, side, body}`. On an update, read what's already there (`gh api repos/<owner>/<repo>/pulls/<number>/comments`) and post only the lines that don't carry a comment yet. Done when every drafted comment is posted.

## Title format

`<type>(<scope>): <subject>`, scope optional.

- Name the **dominant change** of the whole branch, not the latest commit.
- The subject's verb carries the change: `expire sessions after 30 days`, not `update session handling`.
- Plain subject, no trailing period.

## Description template

```md
1–2 sentence summary: what the PR does and why.

A reference to the issue(s) this PR closes (`Closes <id>`).

## Overview

Strictly user-facing: what someone using the app sees or experiences differently. Refactors, component restructuring, and other implementation details belong in Changes. For purely internal PRs, keep it brief ("No user-facing changes."). If there's more than one user-facing theme, add a `###` subheading per theme with short prose under each.

## Changes

Open with the **shape** of the change as a whole — the one view a reviewer reads before the diff. Then a `###` subheading per unit of work with short prose under each, carrying the _why_ the Overview leaves implicit; a one-theme PR is a single paragraph.

Reference a commit by its bare short SHA, which GitHub autolinks.

## Evidence

Captures a reviewer can look at, each referenced inline beneath the prose that says what it proves.

## To-do

What a human must do to land or operate this change: run a migration, set an env var, flip a flag, merge a dependent PR first. Short checkbox bullets (`- [ ]`). Work this PR defers or leaves out of scope belongs in the issue tracker; generic local-testing steps don't belong at all.
```

The `Closes` line, Evidence, and To-do are live only when there's something to put in them.

The description ends with its last live section. No attribution footer, no generated-with line, no link back to the session that wrote it.

## Shapes

A shape carries at a glance what prose would spend a paragraph building. Reach for one when the change moves control flow, introduces a state machine, moves data across more than two modules, runs a sequence across services, or reorganises files broadly. A single-file change is prose.

- **Mermaid**, in a fenced `mermaid` block — flow, state, and sequence. GitHub renders it in the body. Draw it per `/artifact-diagramming`: real states, real names, real branch conditions, arrows labelled with what moves.
- **Fenced text** — a file tree for responsibility or the shape of a broad refactor, a call tree for runtime order, a component tree for UI structure, pseudocode for logic where the branches matter and the syntax doesn't.

## Inline comments

A comment goes where a reviewer stopping at that line would have a question the diff can't answer: the bound that makes a quadratic loop safe, the branch that stays dead until a flag flips, the workaround whose cause lives in another repo.
