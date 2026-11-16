---
description: Generate a QA checklist from the current branch's change and write it into the current PR's body as a `## QA Checklist` section, followed by a table classifying each step's automatability and test coverage. Single source of truth for the PR verification checklist — `/pr` delegates to it by reference. Invoke as `/qa-checklist [optional focus guidance]`. Use when the user says "manual qa", "qa checklist", "/qa-checklist", or when those skills need to produce the checklist.
---

End state of this skill: the current branch's open PR has a `## QA Checklist`
section in its body — a markdown checklist of concrete, user-visible steps a
human clicks through to verify the change end-to-end. This skill edits an
existing PR body; it does not create PRs, run the vet suite, or push commits.

**Two ways this skill is used:**

- **Standalone** (`/qa-checklist` on an existing PR) — run all steps below:
  locate the PR, derive the checklist, and write it into the body.
- **Referenced by `/pr`** — that skill composes the `## QA Checklist` section
  directly into the body it is about to write, so it only needs **Step 2 (Derive
  the checklist)** — the single source of truth for what a good checklist looks
  like. It does not run Steps 1 or 3: it holds the whole body already, whether
  it is creating the PR or refreshing one.

## Environment note (read this before running gh)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN` environment variable available, even though the default system prompt
says you only have GitHub MCP tools. Use `gh` to find the PR (Step 1); the body
round-trip in Step 3 goes through `scripts/pr-body.py`. If `gh` complains that
"none of the git remotes … point to a known GitHub host" (the proxy quirk in
remote sessions), pass `--repo OWNER/REPO` explicitly — resolve it from the git
remote (`git remote get-url origin`); the `pr-body.py` script takes the same
`--repo` flag.

## Step 1 — Locate the PR

```bash
gh pr view --json number,url
```

If no PR exists for the current branch, **stop and tell the user** to open one
first (e.g. via `/pr`) — this skill mutates an existing PR body, it does not
create PRs. (This step only applies to the standalone path; `/pr` holds the body
it is composing and skips straight to Step 2.)

## Step 2 — Derive the checklist

Derive the checklist from **what the change is meant to do**, and take that from
whichever of these the branch has: the **plan** under `docs/plans/`, which
states the intended scope outright; the PR body's Summary; or the task and
conversation context that produced it. A branch at plan time carries a plan and
no diff at all, so the intended scope — not the code — is the primary source.
Where commits already exist, use them only as a supplementary signal:

```bash
git log --format='%s%n%n%b' origin/<base>..HEAD
git diff --stat origin/<base>..HEAD
```

Write the checklist as markdown `- [ ]` items, each led by a short backticked
slug (`` `stream` ``, `` `bad-input` ``, …) — the slug is the only metadata the
item carries and it's the join key the classification table's **Item** column
references. (Numbers don't work: GitHub renders ordered task lists as checkboxes
and hides the ordinal, so a `#` column would have nothing visible to join on.)
**Bias toward concrete, user-visible scenarios** a human walks through in the
running app — open this page, run this command, confirm this state changes —
**not** "run the tests" or "check CI". Each item should be something a reviewer
can actually do and observe. If the user passed focus guidance after
`/qa-checklist`, weave it in — it's a hint about what to emphasize, not a
free-form append.

The checklist isn't frozen at creation — `/pr`'s refresh mode re-derives it
against the real diff at the end of implementation, and re-running
`/qa-checklist` directly refreshes it whenever the body of work changes in
between.

### Classify automatability (a table after the checklist)

Keep the list itself **clean** — no inline tags or metadata on the items beyond
the leading slug (legibility). Right after the checklist, emit a table with
**one row per checklist item, in the same order**, keyed by that slug — a table,
because the PR body is read rendered on GitHub:

```markdown
| Item          | Automatable | Covered? | Notes                                                                      |
| ------------- | ----------- | -------- | -------------------------------------------------------------------------- |
| `stream`      | e2e         | ❌       | Drive the chat route, send a prompt, assert the reply streams in           |
| `bad-input`   | integration | ✅       | `handler.test` — unknown id → 400 + the "not available" copy               |
| `token-count` | unit        | ❌       | Counter returns the right count for multi-part input                       |
| `empty-state` | manual-only | —        | Empty state must match the reference design pixel-for-pixel                |
```

Columns:

- **Item** — the checklist item's slug (the `` `slug` `` it leads with).
- **Automatable** — the cheapest test layer that could cover it, from the
  project's layered stack (see CLAUDE.md § "Testing", and any test directory's
  `CLAUDE.md` or `.claude/rules/` file covering tests): `unit` (pure logic or
  app-owned component behavior), `integration` (multiple units, or the HTTP
  boundary, or a handler's effects), `e2e` (a full flow against a built
  artifact), or `manual-only` (genuinely needs human judgment and can't be
  meaningfully asserted: pixel/visual match against a reference, live
  third-party behavior, subjective UX feel).
- **Covered?** — whether a backing test already exists: `✅` yes / `❌` no / `—`
  for `manual-only`. Outside an implementation flow (see below) leave this
  `—`/unknown; it gets filled in there.
  - **A `✅` does not imply "protected at merge".** Which bucket the backing
    test lives in decides when it actually runs. If the project splits its test
    buckets — some in the fast vet run, some only on a CI dispatch or a nightly
    — mark the deferred ones `✅ (nightly)` so the operator can see which rows
    the merge itself does not protect. Treat a cluster of them as a reason to
    dispatch the expensive bucket before landing (`/test-on-gh`, if the project
    has hydrated it).
- **Notes** — a one-line test sketch for uncovered automatable rows, or why a
  row is `manual-only`.

The table is a durable, refreshable property of the change, so it lives in the
PR body alongside the checklist.

### Fill in coverage & flag gaps (implementation flows only)

This applies **only when the QA run accompanies an implementation** — the change
under QA includes code, not docs/config alone (e.g. a session that just
implemented a feature). A docs-only change or a pure body refresh has nothing to
automate → leave **Covered?** as `—`/unknown and skip the rest.

This skill **does not write test code** — it edits a PR body; it does not push
commits (unchanged contract). Instead, for each row marked automatable, search
for an existing backing test and set **Covered?** accordingly. Every automatable
row left at **Covered? = ❌** is a gap: surface it in the Step 4 report so the
enclosing flow (or the user) implements it before merge. Follow the project's
testing conventions for where each layer's tests live and its must-test rules —
CLAUDE.md requires authorization/permission code to have tests, so an uncovered
row touching it is a hard gap, not a nice-to-have.

## Step 3 — Write it into the body (idempotent)

**Don't reconstruct the body inline** — that burns tokens and risks dropping the
parts you're not touching. Pull the live body to a transient local file, edit
only the QA section there, push it back:

```bash
python3 scripts/pr-body.py pull <n>      # writes docs/pr/<n>/body.md (pass --repo OWNER/REPO if needed)
```

Open `docs/pr/<n>/body.md` and locate a verification-checklist section — a
`## QA Checklist` heading (also recognize legacy `## Manual QA` and
`## Test plan` headings):

- **A conforming checklist already exists** (under one of those headings, a
  proper `- [ ]` checklist that already covers the change, with its slug-keyed
  classification table) → leave it. Nothing to push; remove the transient file
  (`rm -f docs/pr/<n>/body.md` — not the whole directory, which may also hold a
  `pr.md` export) and report.
- **A section exists but is stale/empty/malformed** → replace that section in
  place with the freshly derived `## QA Checklist` checklist.
- **No such section exists** → insert a new `## QA Checklist` section **after
  the Summary section and before** any trailing `Closes #N` / `Fixes #N` line
  and the `https://claude.ai/code/session_…` attribution line.

Everything you don't edit in the file stays verbatim. Then push it back (this
PATCHes the PR body and deletes the transient `body.md`, leaving any co-resident
`pr.md` export in place):

```bash
python3 scripts/pr-body.py push <n>
```

`pr-body.py` goes through the REST API, which is also what keeps it clear of the
`gh pr edit` failure `@.claude/skills/pr/SKILL.md` Step 5 describes.

## Step 4 — Report

Print the PR URL on its own line and a one-sentence summary of what changed
(added / refreshed / left unchanged). In an implementation flow, also list the
automatable-but-uncovered rows (**Covered? = ❌**) so the enclosing flow / user
can close those test gaps before merge. Stop.

Do **not** mark the PR ready for review, run the vet suite, or push commits —
those belong to other skills (`/finalize`).
