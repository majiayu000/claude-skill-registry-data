---
name: learn
description: Capture the post-mortem for a compound-engineering cycle. Reads the issue, PR, review comments, git log, and final diff. Extracts what worked, what changed, what incentives caused friction, what mechanisms improved code health, and what durable rule should be considered. Writes docs/learnings/YYYY-MM-DD-slug.md, commits it, pushes the branch, and hands off to /merge when the PR is still open.
---

# /learn

Before rendering user-facing output, read `../_shared/plain-output.md`.

Close the learning loop.

Capture what was planned, what actually shipped, what the cycle taught, and what mechanism should be preserved or changed.

Do not write a learning file unless there is non-obvious content.

## Preconditions

- A PR exists and normally remains open; merged PRs are acceptable only for historical capture.
- The PR has a linked issue via `Closes #<n>` or equivalent.
- The working tree is clean before writing the learning file:

```bash
git status --porcelain
```

If not clean, stop and ask the user to commit or stash unrelated changes.

- The current branch has a remote upstream or `origin` exists.
- `gh` is authenticated.

## Phase 1 — Gather context

Collect in parallel:

1. **Issue body and metadata**

```bash
gh issue view <n> --json number,title,body,state,url
```

2. **PR metadata and diff**

```bash
gh pr view <n> --json number,title,body,state,mergedAt,url,baseRefName,headRefName,headRefOid,baseRefOid
gh pr diff <n>
```

3. **Review threads**

Use the GraphQL `reviewThreads` query from `/address` when available. Include resolved status, reviewer, body, path, line, and replies.

4. **PR review comments and issue comments**

```bash
gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate
gh api repos/{owner}/{repo}/issues/<n>/comments --paginate
```

5. **Git log for the branch**

```bash
git log --oneline <base>...<head>
```

or:

```bash
git log --oneline origin/main..HEAD
```

when base is main and branch comparison is clear.

6. **Existing learning files**

Read `docs/learnings/` if it exists.

## Phase 2 — Analyze with parallel explorer subagents

Read `../_shared/subagents.md` and `../_shared/evidence-quality.md`.

Use host-neutral explorer subagents. Spawn four explorer subagents in parallel when the host supports subagents. Give each the context bundle from Phase 1. If subagents are unavailable, run the four lanes locally and state that parallel analysis was unavailable.

The main agent decides whether the lesson is real enough to write; subagents provide evidence and analysis only.

### Agent A — What actually ended up working

Compare the issue’s Architecture section with the final code.

Report what matches, what changed, why it changed, whether the ASCII diagram still describes reality, and replacement diagram if needed.

Return 150–300 words.

### Agent B — What surfaced in review

Summarize review threads: how many addressed, pushed back, escalated; recurring categories; which comments changed the final design. For each pushback, state the one-line reason.

Return 100–200 words.

### Agent C — Non-obvious lesson and pattern

Find what a thoughtful engineer would not have known before doing this cycle.

Report:

- the non-obvious lesson
- reproducible pattern, if any
- one-sentence AGENTS.md amendment candidate, if any

Return:

```markdown
Lesson:
<paragraph>

Pattern:
<3-5 lines or None>

AGENTS.md amendment candidate:
<one sentence with Why: clause, or None>
```

### Agent D — First-principles and game-theory postmortem

Analyze the cycle as a mechanism.

Report:

- what invariant mattered most
- what assumption changed
- what local incentive caused friction
- what mechanism improved alignment
- what information was missing early
- what bad equilibrium was avoided or discovered
- what future review should check sooner

Return 150–250 words.

## Phase 3 — Decide whether to write

Do not create a learning file if all agents conclude:

- everything went as architected
- no review finding changed the result
- no non-obvious lesson emerged
- no durable mechanism/incentive lesson exists

If no file is warranted, say so and stop without committing.

## Phase 4 — Assemble the file

Write to:

```text
docs/learnings/YYYY-MM-DD-<slug>.md
```

Use today’s date from:

```bash
date +%Y-%m-%d
```

Slug is a kebab-case version of the issue title, trimmed to fewer than 50 characters.

If `docs/learnings/` does not exist, create it.

If the PR is not yet merged, prefix the `type` frontmatter value with `in-flight-`.

File contents:

````markdown
---
date: YYYY-MM-DD
type: bug | feature | refactor | decision | in-flight-bug | in-flight-feature | in-flight-refactor | in-flight-decision
topic: <one-line from issue title>
issue: <issue url>
pr: <pr url>
---

# <topic>

## Decision

<One sentence: what we learned and whether it should change future behavior.>

## What changed

<What was planned vs what shipped. Include an updated ASCII diagram only if reality changed.>

## Why it mattered

<Invariant, assumption, source of truth, or incentive that became clearer.>

## Example

```ts
<small code, command, diff, or pseudocode example that shows the pattern>
```

## Rule candidate

<AGENTS.md amendment candidate, or "None".>

This is a proposal. Review and edit AGENTS.md yourself if you want to adopt it — `/learn` never auto-edits AGENTS.md.
````

## Phase 5 — Commit and push

After writing the file:

1. Stage only the learning file:

```bash
git add -- docs/learnings/YYYY-MM-DD-<slug>.md
```

2. Commit it:

```bash
git commit -m "docs: capture learning for #<issue>"
```

3. Push the current branch:

```bash
git push
```

If no upstream exists:

```bash
git push -u origin "$(git branch --show-current)"
```

Do not include unrelated files in the commit.

If the commit or push fails, surface the exact error and stop.

## Output

Use Plain Senior output:

````markdown
## Decision
Learning captured in <path>.

## Why
lesson=<one-line durable lesson>
mechanism=<one-line mechanism/incentive lesson>

## Example
```bash
git show --stat <sha>
```

## Risk
<open PR state, skipped amendment, or "None known">

## Next
<handoff line below>
````

Then:

- If the PR is open, end with exactly this line and stop:

> Cycle captured at <path> in <sha>. Run `/merge` to merge the PR and clean up the branch.

- If the PR is already merged or closed, end with exactly this line and stop:

> Cycle captured at <path> in <sha>. Loop complete.

## Rules

- Do not write the file if Agent A, B, C, or D failed to produce content.
- Do not auto-apply AGENTS.md amendments.
- Do not create a learning file if the issue/PR carries no non-obvious content.
- Never commit if no learning file was written.
- Never commit unrelated working tree changes.
- Preserve the difference between:
  - what was planned
  - what shipped
  - what was learned
  - what mechanism should change
