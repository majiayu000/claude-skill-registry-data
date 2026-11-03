---
name: readme-status
description: Content-editor-posture skill that brings a product README's Status section up to what is built. One run reduces the product's what-left file against the tip of main, removing only the entries whose whole want has merged, then rewrites the Status section from the reduced file, every built sentence citing the commit that brought it in, and makes one commit in the product's repository. Writes no other file and never adds an entry. Halts outside Content Editor posture. Run when a product has merged work and its README Status section may be out of date.
license: MIT
metadata:
  version: "1.2.0"
---

# readme-status

**The prompt owns judgment, and this file owns the loop.** `prompts/thin.md` decides which wants are
wholly built, which commit brought each in, and what the Status section says. This file resolves the
product, validates both targets, builds both results from original bytes and makes the one commit.
It reads that one prompt and no other judgment body. That prompt also carries the published
sentence shapes and outcome messages; the posture refusal below runs before it is read.

## When to Use

- A product has merged work and its README `## Status` section, or its what-left file, may no longer
  say what is built. Start it with `<CORE>/launchers/skill/launcher.sh readme-status <project>`.
- **Content Editor role only.** Outside a `content-editor` session or subagent, the run changes no
  file, makes no commit, and its final message says it needs Content Editor posture and to open a
  session or subagent as `content-editor`. It reads no project input first, the same refusal the
  seat's other skill gives (`<CORE>/roles/loaders/content_editor_global.md`, *Skills toolbox*).

**Refused for posture — the session is not a Content Editor session**

> readme-status changed no file and made no commit.

> It needs Content Editor posture.

> Open a session or subagent as `content-editor` and run readme-status again.

**Do not use for:**
- Adding, rewording or reordering a what-left entry. An entry is added by whoever changes the Agari
  or PRD (`<CORE>/doctrine/setup/kensaiapp_structure.md` § 3, *The what-left file*).
- Editing a README outside its Status section, or creating a README.
- The words of one change. That is `development-content`'s, with its own inputs and output.
- Writing or amending a standing wording rule. A rule the Status section needs and the standard lacks
  is a finding in the final message, for the Content Manager.

## Input

**The project** — `<project>`, one name. The change folder, a change key and a halt report are not
inputs and the run never reads them.

## Workflow

Run from the instance root. After the posture gate, read `prompts/thin.md` for the judgment and
the outcome sentences. A pre-write refusal changes no file and makes no commit; its final message
opens with the refusal sentence and names the condition that held. A commit-builder refusal uses
the separate message that says the files were written and remain uncommitted.

### 1 — Resolve the destination

Read `system/projects/<project>/project.md`. Refuse if there is no card, or no `Product path:` line.
Resolve `Product path:` as the launcher does: relative against the instance, absolute directly, `~`
expanded. Refuse if no directory is there. Find the repository holding it with
`git -C <product> rev-parse --show-toplevel`, and refuse if there is none. That checkout must already
be on `main`. Never switch a branch and never open a change worktree. A product in another
repository commits there, and an in-repo product commits in the containing instance repository.

### 2 — Read and validate, before any write

Read the what-left file at `<product>/docs/what_left.md`, to the grammar and the readings of
`<CORE>/doctrine/setup/kensaiapp_structure.md` § 3 (`:2301-2307`), and `<product>/README.md`. Refuse
for each of these, one condition at a time:

- the what-left file does not exist (never given), or holds neither an entry nor the empty marker, or
  holds both;
- an entry lacks a `**Wanted:**`, `**Source:**` or `**Missing at:**` line, or its `Missing at` commit
  is not carried by `main`;
- the README does not exist, or does not have exactly one line reading `## Status`;
- either target has uncommitted changes, or an unrelated path is staged;
- `main` is unavailable, or any other condition that makes either rewrite impossible.

Record the original bytes of both targets, `main`'s tip and the exact start and end of the Status
body. Read the product's `docs/CONTENT.md`, or `system/doctrine/writing_bar.md` when it has none.

### 3 — Judge

Evidence a product check needs runs in a **disposable copy** — a fresh clone at the commit under test
(`git clone --quiet <repo> <scratch> && git -C <scratch> checkout --quiet <sha>`; never `git archive`, which drops the history a check may read), never in the target checkout (`<CORE>/roles/CROSS_ROLE.md`
§ *Every seat — a run leaves the product's main checkout as it found it*). Run the checks from a subshell, never `cd` your own shell into the copy, and remove the copy when you have read the result, in a command of its own run from outside it. Apply `prompts/thin.md`
to the judgment with the retained entries, the evidence, the original Status text and the standard. A
refusal it returns for a built want with no establishable commit is acted on here, before any write.

### 4 — Build both candidates, then check them

Prepare one candidate pair plus the transient evidence before any target write.

- The what-left result removes only the selected original three-line entry spans. The H1 and lead
  sentence stay byte-identical. When the last entry goes, the file holds the line
  `Nothing is left to build.` alone. The file is never deleted.
- The README result replaces only the Status body: from after the `## Status` line to before the next
  line starting `## `, or the end of the file.
- Compare the unchanged bytes outside the two edits. A zero-length old hunk range is an insertion
  point after the heading and before the next heading, including an empty Status body.
- Check that every retained want is represented as not built, that each built sentence carries its own
  nine-hexadecimal commit in an inline code span, with `git merge-base --is-ancestor <sha> main` true
  for each, and that no term the standard rejects is used.

### 5 — Re-check, then commit once

Immediately before the first write, re-check `main`'s tip, both original byte sequences, the targets'
cleanliness and the staged set. Refuse on a changed input, a moved `main`, or an unrelated staged path.

If both candidates are byte-identical to their inputs, make no commit and report that nothing changed.

Otherwise write only the changed targets and make **exactly one commit** through
`<CORE>/tools/commit_builder.py`, following `<CORE>/doctrine/governance/commit_via_builder.md`:
`--repo` is the product's repository, the staged files are the changed targets only,
**`--actor content-editor`**, **`--skill readme-status`**, the runtime's surface and identity, and
`--reasoning-effort` when the launch resolved one. The directional line follows
`<CORE>/doctrine/governance/commit_format.md` § Directional trailer. The body carries one line per
removed entry, `Merged in <commit>: <the entry's Wanted text, verbatim>`; write the body through a
file, because Wanted text may hold backticks and shell metacharacters. When the builder refuses, say
so in the final message, with its message verbatim. Use no empty commit, no index waiver and no second
commit to get past it.

## Final message

The one outcome (changed, nothing changed, or a refusal), every built claim left out because no
commit could be established, and any wording rule the standard lacks, in the sentences of
`prompts/thin.md`. All findings stay in the final message. The run writes no report file, writes
nothing in a satellite and writes no file but the two targets.

## Critical Rules

- **Content Editor posture only**, checked before any input is read.
- **Only the two targets are written**, only on `main`, in one commit.
- **Never add, reword or reorder an entry.** Reducing is all this run does to the file.
- **No built sentence without its own commit**, established by first-parent before and after evidence.
- **Evidence runs in a disposable copy**, never in the target checkout.
- **Every core reference is `<CORE>`.** The method is `prompts/thin.md`; this file restates neither
  the grammar, the commit recipe nor the seat's wording rules.
