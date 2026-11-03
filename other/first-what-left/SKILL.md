---
name: first-what-left
description: CPO-posture skill that writes a product's first what-left file, docs/what_left.md, once the project's Agari is settled. One run checks eight conditions in a fixed order, and the first that holds stops it with no file written. Otherwise it reads the Agari and the PRD, keeps each want the product's code can be shown not to do at the tip of main and drops each want only the owner's judgement can pass, writes the file in the shape of the what-left template, and makes one commit of that file in the product's repository. Never edits an existing list. Halts outside CPO posture. Run once for a project whose product has no what-left file yet.
license: MIT
metadata:
  version: "1.1.0"
---

# first-what-left

**The prompt owns judgment, and this file owns the loop.** `prompts/thin.md` decides which wants
qualify, how an entry is worded and what every final message says. This file resolves the product,
runs the checks in order, builds the file and makes the one commit. It reads that one prompt and no
other judgment body. The posture refusal below runs before the prompt is read.

## When to Use

- A project's Agari is settled and its product has no `docs/what_left.md`. Start it with
  `<CORE>/launchers/skill/launcher.sh first-what-left <project>`.
- **CPO role only.** Outside a `cpo:` session or the `cpo` subagent, the run writes no file, makes no
  commit, and its final message says it needs CPO posture. It reads no project input first.

**Refused for posture — the session is not a CPO session or the `cpo` agent**

> first-what-left wrote no file and made no commit.

> It needs CPO posture.

> Open a session or subagent as `cpo` and run first-what-left again.

**Do not use for:**
- Adding, rewording, reordering or removing an entry in a list that exists. The run leaves any
  existing list as it is (`<CORE>/doctrine/setup/kensaiapp_structure.md` § 3, *The what-left file*).
- Writing the Agari or the PRD (`project-agari`, `product-prd`).
- A product whose card names a nominal Product path. The run writes only inside a product's own `docs/`.

## Input

**The project** — `<project>`, one name. The run asks no question.

## The checks, in order

Run from the instance root. The first condition that holds decides the run: it writes no file anywhere,
makes no commit in any repository, and its final message opens with the refusal sentence and gives the
sentences of that condition, from `prompts/thin.md`. Items 1 to 6 are the conditions in that order,
and items 7 and 8 follow them, still before any write.

1. `project.md` — read `system/projects/<project>/project.md`. Refuse if there is no card, or the card
   has no `**Product path:**` line. Resolve the value as every stage does: relative from the instance
   root, absolute as written, a leading `~/` as the home directory. The result is `<product>`.
2. `nominal` — read `<CORE>/doctrine/setup/kensaiapp_structure.md` § 1 *Instance-level* now, to get the
   directories it places in the instance itself. Never copy that list into this file or into a note.
   Resolve `<product>` and the instance root to real paths, and compare by prefix. Refuse when
   `<product>` is the instance root, or is at or under one of those directories. A path outside the
   instance, or in an instance directory § 1 does not claim, names a product.
3. `docs/what_left.md` — refuse if `<product>/docs/what_left.md` exists, whatever it holds. Do not read
   it.
4. `agari.md` — refuse if `system/projects/<project>/agari.md` does not exist.
5. `agari_open_issues.md` — refuse if `system/projects/<project>/agari_open_issues.md` exists. The Agari
   is settled only when `agari.md` exists and this companion does not.
6. `docs/PRD.md` — refuse if `<product>/docs/PRD.md` does not exist, whether the file or the whole
   product directory is missing.
7. `git` — find the repository holding `<product>` with `git -C <product> rev-parse --show-toplevel`.
   Refuse if there is none, or if that repository has no `main` branch.
8. `staged` — refuse if `git -C <checkout> diff --cached --name-only` lists any path. The run's commit
   may hold only the one file, and the builder's staged-set guard would refuse after the write.

Any other condition that stops the run before a write is refused in the closing sentence of
`prompts/thin.md`'s refusals.

## Workflow

After the checks pass, read `prompts/thin.md`.

### 1 — Record `main`

Record `main`'s tip once with `git -C <checkout> rev-parse main`, and write its first nine hexadecimal
digits down as `<tip>`. Never switch a branch and never open a worktree. Every want is judged at that
one commit, so every entry shares one `**Missing at:**` value.

### 2 — Read and judge

Read `system/projects/<project>/agari.md` and `<product>/docs/PRD.md`. Judge each want they state by
`prompts/thin.md`. Evidence comes from `git -C <checkout> grep … <tip> -- <sub>`, where `<sub>` is
`<product>` relative to `<checkout>`, which needs no copy. Code is run only in a disposable copy — a fresh
clone at `<tip>` (`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <tip>`; never `git archive`,
which drops the history a check may read), never in the product's checkout
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat*). Run the checks from a subshell, never `cd` your own shell into the copy, and remove the copy when you have read the result, in a command of its own run from outside it. A want only the owner's judgement can pass gets no entry.

### 3 — Build the file

Shape it by `<CORE>/templates/product-templates/what_left_template.md`: the H1 heading and the lead
sentence, then one or more entries or the empty marker `Nothing is left to build.`, never both and
never neither. No `<…>` placeholder and no HTML comment survives. The product name in the heading is
the PRD's H1, and the project name where the PRD gives none. Check the candidate before writing: each
entry has the three labels exactly, each `Source` names a section heading that exists in its
document, and each `Missing at` is `<tip>` and passes
`git -C <checkout> merge-base --is-ancestor <tip> main`.

### 4 — Re-check, write, commit once

Re-check `test -e <product>/docs/what_left.md` just before writing, and `main`'s tip. Refuse with the
sentence of that state if the file has appeared. Write `<product>/docs/` first if it is missing, then
write only that one file.

Make **exactly one commit** through `<CORE>/tools/commit_builder.py`, following
`<CORE>/doctrine/governance/commit_via_builder.md`: `--repo` is the product's repository
(`<checkout>`), `--add` is that one file's path relative to `<checkout>`,
**`--actor cpo`**, **`--skill first-what-left`**, the runtime's surface and identity, and
`--reasoning-effort` when the launch resolved one. The directional line follows
`<CORE>/doctrine/governance/commit_format.md` § Directional trailer. Write the body through a file.
When the builder refuses, say so in the final message with its message verbatim. Use no empty commit,
no index waiver and no second commit to get past it.

## Final message

The one outcome, in the sentences of `prompts/thin.md`: a refusal, the builder refusal, or the
completion message, followed by one sentence for each want the list leaves out. The run writes no
report file, writes nothing in a satellite and writes no file but `<product>/docs/what_left.md`.

## Critical Rules

- **CPO posture only**, checked before any input is read.
- **The first condition that holds decides the run**, in the order of the checks list.
- **Only `docs/what_left.md` is written**, only inside a product's own `docs/`, in one commit.
- **An existing list is never read, changed or replaced.**
- **A want only the owner's judgement can pass gets no entry.**
- **Evidence runs in a disposable copy**, never in the product's checkout.
- **Every core reference is `<CORE>`.** The method is `prompts/thin.md`; this file restates neither the
  file's grammar nor the commit recipe.
