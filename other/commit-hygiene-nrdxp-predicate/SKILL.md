---
name: commit-hygiene
description: |
  Rules, conventions, and constraints for formatting git commit messages and committing at logical boundaries.
  Trigger when:
  - Drafting, revising, or validating git commit messages.
  - Pausing at commit boundaries under the CORE or CONTINUE workflows.
  - Evaluating whether a changeset should be split into multiple commits.
  - Prompt contains keywords: commit message, git commit, conventional commits, commit hygiene, commit guidelines, logical boundary, spaghetti diff, atomic commit, commit boundary.
---

# Commit Hygiene

Guidelines and constraints for writing clear, structured, and reviewer-centric git commit messages. Every commit is a unit of structured information designed to optimize human comprehension and git history utility.

## Purpose

The goal of commit hygiene is not formatting for its own sake. The goal is a **clean, human-reviewable git history**.

A well-maintained history lets a human reviewer reconstruct the reasoning behind a codebase by reading `git log`. Every commit should answer: *what changed, why it changed, and where the logical boundary of that change is.* When history achieves this, it becomes a durable decision record — not just a log of file mutations.

This requires two things working together:

1. **Good commit messages** — clear, structured, motivated (covered by the formatting and communication rules below).
2. **Commits at logical boundaries** — each commit captures one coherent unit of change with a reviewable diff (covered by the Atomicity and Boundary Discipline section below).

Neither is sufficient alone. A perfectly formatted message attached to a 40-file spaghetti diff is useless. A clean single-file diff with a message that says "update stuff" is nearly as bad. Both disciplines are required, always — not only when a formal workflow like C.O.R.E. is active.

## Hard Constraints

All commit messages MUST satisfy these structural invariants:
1. **Header Line Limit:** The summary line MUST NOT exceed **50 characters**.
2. **Body Line Limit:** No line in the body or footer may exceed **72 characters**.
3. **Blank Line Separation:** A single blank line MUST separate the header from the body.

---

## Conventional Commits Structure

Commits must conform to the Conventional Commits v1.0.0 specification:

```
<type>(<scope>)[!]: <description>

[optional body]

[optional footer(s)]
```

### Breaking Changes

A breaking change must be indicated by:
- An exclamation mark `!` suffixing the type or scope in the summary header (e.g., `feat!: remove deprecated api` or `fix(parser)!: adjust breaking parser logic`).
- A `BREAKING CHANGE: <description>` footer entry.

### Allowed Types

- `feat`: Introduction of a new capability or feature.
- `fix`: Resolution of a bug or regression.
- `docs`: Additions or modifications to documentation.
- `style`: Formatting, whitespace adjustments, or cosmetic corrections (no functional change).
- `refactor`: Structural codebase changes that neither modify behavior nor add features.
- `perf`: Optimizations that improve execution speed or resource utilization.
- `test`: Addition, restructuring, or correction of tests.
- `build`: Modifications to build configuration, dependencies, or packaging (e.g. `Cargo.toml`, `package.json`, `go.mod`).
- `ci`: Alterations to CI pipeline or automation configurations.
- `chore`: Auxiliary tasks, infrastructure tooling updates, or miscellaneous maintenance.
- `revert`: Reversion of a previous commit.
- `merge`: Integration of one branch, pull request, or workstream into another.
  (On forge-hosted projects, merges follow the [forge discipline](../forge/SKILL.md):
  consent-to-merge, self-contained PR prose, review-on-record.)

### Merge Commits

Use `merge:` for any commit whose primary purpose is integrating a branch or
pull request:

```
merge: integrate the payment-retry branch
```

The same hard constraints apply: the header must not exceed 50 characters, a
blank line must separate header from body, and body lines must not exceed 72
characters. A body is encouraged when the integration is non-trivial — what
conflict was resolved, what design decision the merge closes.

**Distinction from the recorder convention.** The `.ledger/log/` flight-log uses
`log:` subjects for its own sketch commits. `log:` is a recorder-only convention
scoped to that sub-repository and does not appear in working-repository commits.
`merge:` is a working-repository type and does not appear in the recorder.

**Auto-generated merge subjects are not valid.** Git's default `Merge branch
'foo'` and `Merge pull request #N` subjects do not carry a conventional type and
will fail the validator. Replace them with a `merge:` header that names *what*
was integrated and *why* it landed when the merge was not self-evident.

### Summary Header Formatting

- **Imperative Mood:** Use active, imperative verbs ("add", "fix", "refactor", "remove") rather than past-tense or present-participle ("added", "fixing", "refactored", "removes").
- **No Trailing Period:** The header line must not end with a period.
- **Lower Case:** The description after the colon should start with a lowercase letter (unless referencing a proper noun or acronym).

---

## Human-Centric Communication

Commits are written for human reviewers, not systems. Prioritize cognitive clarity:

### Focus on "Why" and "What"

- **The "Why":** Explain the motivation behind the change. What problem is this resolving? What context is required to understand this design decision?
- **The "What":** Describe what was changed at a conceptual level. Avoid summarizing the raw code diff (which the reviewer can already see); instead, describe the logical transition of the system.
- **Explain the Tradeoffs:** If a non-obvious design pattern or workaround was employed, document it honestly.

### Self-Contained Messages — No Contextless References

Commit messages must be **self-contained**. A reviewer reading
`git log` has access to exactly two things: the repository's
committed history and the public internet. If a reference in a
commit message cannot be resolved from one of those two sources,
it is meaningless noise.

- **No Uncommitted Artifacts:** Planning documents, sketches,
  scratch files, and workstream trackers (`.ledger/`,
  `.scratch/`, agent scratch pads, etc.) are **never committed
  to history**. Referencing labels that originate from these
  artifacts — workstream items like "(P3)", sketch IDs, plan
  phase names, task-tracker shortcodes — is **prohibited**.
  These tokens carry zero information for any reader who did
  not have the ephemeral document open. Describe the *actual
  change and its motivation* instead.
- **No Workflow/Agent Idiosyncrasies:** Do not reference
  internal workflow states, subagent execution steps, or
  transient, agent-specific planning phases (e.g., "resolving
  step 4 of the execution plan"). These are equally opaque.
- **Independently Derivable Information:** Every reference in a
  commit message must resolve to something a human reviewer can
  independently locate — a committed file path, a prior commit
  SHA, an issue number in a linked tracker, or a URL. If a
  reviewer cannot follow the reference, it must not appear.
- **Direct Links for External Context:** When referring to
  requirements, design decisions, or documentation, use paths
  to committed files (e.g., `skills/commit-hygiene/SKILL.md`)
  or full URLs. If the context is not committed and not on the
  public internet, paraphrase it inline instead of citing it.

### Atomicity and Boundary Discipline

- Each commit must represent a single, cohesive logical change.
- **Proactive boundary identification:** Before beginning a task, identify the natural commit boundaries. If a task involves multiple logical steps (e.g., "add a type, then update callers, then add tests"), each step is a candidate boundary. Do not defer this judgment to the end — plan where you will commit before you start writing code.
- **Reviewable diffs:** Every diff attached to a commit must be reviewable by a human in one sitting without losing the thread. If a diff touches many files across unrelated concerns, it has crossed a boundary that should have been a separate commit.
- **Anti-pattern — spaghetti diffs:** Massive, entangled diffs that span multiple logical changes are the primary failure mode of git history. They make review impossible, bisect useless, and revert dangerous. Avoiding them is not optional.
- **Anti-pattern — "and" commits:** If a commit message requires the word "and" to describe its change (e.g., `feat: add user login and fix lint errors`), evaluate whether it should be split.
- **This applies universally.** Logical boundary discipline is a de facto standard for all codebase work — not a feature of any specific workflow. C.O.R.E. formalizes it with explicit commit gates, but the underlying obligation exists whether or not C.O.R.E. is active.

---

## Mechanical Validation

The hard constraints are deterministic, so they are enforced by an
evaluator, not by recall. Before every commit (and after, when auditing
history), run:

```bash
python3 skills/commit-hygiene/scripts/check_commit_msg.py --message "<msg>"
python3 skills/commit-hygiene/scripts/check_commit_msg.py --file <msgfile>
python3 skills/commit-hygiene/scripts/check_commit_msg.py --ref HEAD
```

Exit `0` is required to proceed. Errors (`E1`–`E5`) cover the header
limit, Conventional Commits structure, trailing period, blank-line
separation, and body line length (URL-bearing lines exempt). Warnings
(`W1`–`W2`) flag probable case/mood issues but do not fail — they need
human judgment (proper nouns, unusual verbs). If the script is missing
or fails to execute, fall back to the manual checklist below; never
skip validation silently.

---

## Commit Checklist

Before presenting a commit, run this audit:

### Message Quality
- [ ] Is the header length ≤ 50 characters?
- [ ] Are all body and footer lines ≤ 72 characters?
- [ ] Is there a blank line between the header and the body?
- [ ] Is the header in the imperative mood?
- [ ] Does it use a valid Conventional Commit type?
- [ ] Does the body explain the *why* and *what*, rather than just reproducing the diff?
- [ ] Are breaking changes explicitly denoted using `!` in the header and/or a `BREAKING CHANGE: <description>` footer?
- [ ] Is the message self-contained? Does it avoid references to
      uncommitted artifacts (sketches, scratch files, workstream
      labels like "P3") and use only committed paths, commit SHAs,
      tracker issue numbers, or URLs?

### Boundary Discipline
- [ ] Does this commit represent a single, cohesive logical change?
- [ ] Is the diff reviewable by a human without losing the thread?
- [ ] Does the commit avoid mixing unrelated concerns?
- [ ] If the message needs "and" to describe the change, should this be split?
