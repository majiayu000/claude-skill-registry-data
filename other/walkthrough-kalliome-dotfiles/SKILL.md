---
name: walkthrough
description: Story-driven PR walkthrough published as an HTML preview. Finds the user stories inside a change set, walks each one through how the user triggers it and how the data flows, shows the code diff per file with an explanation of what was done and why, and groups mechanical churn at the end.
argument-hint: "[focus-area]"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, Skill, AskUserQuestion
---

# PR Walkthrough Skill

Produce a walkthrough of the current change set as a published HTML page, built
with the **preview** skill. The walkthrough is organised around the *stories*
inside the PR — user-facing capabilities or flows — not around the file list.
Each story is told the way a reviewer experiences the product: what the user
does, what happens to the data, and then the actual diffs per file with an
explanation of what was done and why. Repetitive mechanical changes are swept
into a grouped section at the end so they don't drown the stories.

## Configuration

**Focus Area (Optional):** $ARGUMENTS

If provided, filter the walkthrough to changes related to the focus area
(e.g. "authentication", "src/api/", "payment processing") and say so at the
top of the page.

## Step 1: Verify Git Repository

```bash
git rev-parse --git-dir 2>&1
```

If this fails, tell the user this directory is not a git repository and that
the skill needs one (navigate to a repo or `git init`), then stop.

## Step 2: Detect Branch Context

```bash
git branch --show-current
git rev-parse --verify main 2>/dev/null || git rev-parse --verify master 2>/dev/null
```

- On `main`/`master` → analyze uncommitted changes only: `git diff HEAD`.
- On a feature branch with `main` (or `master`) → `git diff main...HEAD`.
- No main/master → compare to the default branch, or ask the user.

Call the chosen range `$RANGE` below (empty range = `HEAD` for uncommitted
changes).

## Step 3: Gather Changes

```bash
git diff --name-status $RANGE
git diff --stat $RANGE
git diff $RANGE
```

Also capture the commit messages in the range (`git log --oneline $RANGE`
style) — they often name the stories for you.

Read the current version of every meaningfully changed file (or the relevant
parts) so explanations come from understanding the code, not just the diff
hunks.

## Step 4: Find the Stories

This is the heart of the skill. Cluster the changes into **stories** — coherent
units a reviewer can hold in their head. A story is one of:

- **A user story**: something a user can now do, or does differently.
  Title it in user-story form: *"A user can reset their password from the
  login screen"*, not *"Changes to auth module"*.
- **A data-flow story**: for backend/infra changes with no visible UI, the
  journey of a piece of data: *"Order events now flow through the outbox
  table before hitting the queue"*.

Rules for clustering:

- Aim for **1–5 stories** per PR. If you find more, some are probably the same
  story or belong in the mechanical bucket.
- Assign every changed file to exactly one story **or** to the mechanical
  bucket (Step 6). Nothing gets silently dropped — a coverage check at the end
  must account for every file in `--name-status`.
- The **mechanical bucket** catches wide, same-shaped churn: renames and moved
  imports, lockfiles and generated code, formatting-only diffs, version bumps,
  a one-line signature change rippled through many call sites, test snapshot
  updates. The test: if the tenth file teaches the reviewer nothing the first
  file didn't, it's mechanical.
- Use commit messages, route/handler names, and UI entry points to name
  stories. Only use AskUserQuestion if the purpose of a large change is
  genuinely ambiguous after reading the code.

## Step 5: Tell Each Story

Each story becomes one `<section>` on the page with a stable kebab-case id,
containing in order:

1. **The story** — one short paragraph: who does what, and why this change
   exists.
2. **The walkthrough** — how the user moves through it, or how the data flows.
   Narrate it as a sequence: *user clicks X → handler Y validates → service Z
   writes → …*. Ground every step in the actual code: name the function,
   route, or component that handles it.
3. **A mermaid diagram** of the flow — sequence diagram for interactions,
   flowchart for data pipelines. Mark which nodes are new vs. modified. Skip
   the diagram only when the story is a trivial one-file change.
4. **Per-file diffs with explanations** — for every file in the story, in the
   order the flow visits them:
   - A heading with the file path and change type (added/modified/deleted).
   - **What was done** and **why** — 2–5 sentences of prose. The "why" is the
     valuable half: what problem it solves, why this approach, what it
     connects to in the other files of this story.
   - The **actual diff** for that file (`git diff $RANGE -- <path>`), rendered
     as described under "Diff rendering" below. Long diffs (> ~80 lines) go
     inside a collapsed `<details class="acc">`; short ones stay open.

## Step 6: Supporting Changes (the mechanical tail)

After the stories, one section (e.g. `id="supporting-changes"`) for the
mechanical bucket, grouped **by type of change**, not by directory:

- One group per pattern: *"Import path updates after the module rename
  (23 files)"*, *"Lockfile and dependency bumps"*, *"Snapshot updates"*.
- Each group gets: one shared explanation of what was done and why (once, not
  per file), the full file list, and **one representative diff** open plus the
  rest collapsed in accordions. For truly identical churn (lockfiles,
  generated code) the file list alone is enough — say so explicitly.

## Step 7: Build and Publish the Preview

Invoke the **preview** skill (Skill tool, `skill: "preview"`) and follow it —
slug naming (`<project>-walkthrough-<topic>`), `base.css` or inherited project
tokens, `<section>` ids, mermaid via `/_assets/mermaid.min.js`, self-check,
and narration. Walkthrough-specific guidance on top of it:

**Page structure:**

1. **TL;DR callout** at the top: branch, base, files changed, and the list of
   stories in one line each — the 10-second version of the PR.
2. One section per story (Step 5), in order of importance.
3. The supporting-changes section (Step 6).
4. A short **review guide** at the end: what to look at most carefully, what
   should be tested, known risks.

**Diff rendering:** render diffs in a `<pre class="diff">` block with
page-local CSS in the story sections. HTML-escape the diff text, then wrap
lines in spans: additions (`+`) tinted with `--ok`, deletions (`-`) with
`--danger`, hunk headers (`@@`) with `--muted` — background tints ≤ 8%, no
extra borders or shadows, monospace from `--mono`. Keep the `+`/`-` markers in
the text so the diff is copy-pasteable. Give the block `overflow-x: auto`.

Line spacing must look like a terminal diff — **no gaps between lines**. The
bug to avoid: a `display: block` span *plus* a literal newline after it inside
`<pre>` renders as the line and then a blank line. Pick one line-break
mechanism, never both:

- Preferred: keep spans **inline** (default display, no width/margin/padding)
  and let the single `\n` after each span be the only line break:
  `<span class="add">+foo</span>\n<span class="del">-bar</span>\n`.
- If a line needs a full-width background, make spans `display: block` and
  emit them with **no whitespace between** them in the HTML source.

Set `line-height` ≈ 1.4–1.5 on the block and zero vertical margin/padding on
line spans. Verify in the rendered page (visual iteration step) that diff
lines sit flush before publishing.

**Narration:** a PR walkthrough is substantial — write `narration.md` and run
narrate per the preview skill. The script tells the stories and the review
guide; it never reads diffs aloud.

## Step 8: Reply in the Terminal

End with a short summary: the stories found (one line each), the size of the
mechanical tail, and the preview link `https://preview.teppo.dev/<slug>/`.
Do not duplicate the full walkthrough in the terminal.

## Style Guidelines

- The story order is the reviewer's reading order — put the riskiest or most
  interesting story first.
- Explain the "why" over the "what"; the diff already shows the what.
- Every step of a flow narrative names real code (`file.ts:line`, function,
  route) so the reader can jump from prose to diff.
- Never pad: a one-story PR gets a one-story page.
