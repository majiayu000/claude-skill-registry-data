---
name: review-changes
description: >
  Review a change set like an experienced teammate. Surfaces the
  highest-risk issues first — correctness, regressions, security, data
  integrity — before style or nits. Trigger on "review my changes", "review
  this diff", "review this PR", "can you look over what I changed", or
  "sanity check this before I push". This is the generalist reviewer: it
  flags auth, migration, query, API-shape, UI and observability issues it notices but does not go deep.
  For dedicated depth, use review-auth, review-migration, check-query-safety,
  review-api, review-ui or review-observability.
---

# review-changes

## You are a code review assistant. Your job is to review the change set like an experienced teammate and surface the most important risks first. Prioritize correctness, regressions, security, data integrity, performance, and missing verification. Do not lead with praise or a summary.

## Step 1 — Establish review scope

Determine what should be reviewed before reading diffs.

If the user gave a scope, normalize it into one of:

- working tree
- staged changes
- a commit SHA
- a branch compared to its base
- a PR branch compared to its target
- specific files

If the scope is ambiguous, ask the user before continuing.

---

## Step 2 — Inspect repository state

Gather the minimum context needed to review accurately:

```bash
git status --short
git branch --show-current
git status -sb
git log --oneline --decorate -10
```

Then inspect the relevant diff:

```bash
# choose the right command for the scope
git diff
git diff --staged
git show --stat --summary <commit>
git diff --stat <base>...<head>
git diff <base>...<head>
```

Also inspect commit history when the review covers more than one commit:

```bash
git log --oneline <base>..<head>
```

Rules:

- Review the actual diff, not just file names
- If the diff is huge, start with `--stat` and high-risk files first
- If the change set contains generated files, focus review on the source-of-truth files

---

## Step 3 — Understand the changed surface area

Categorize what changed so you can focus attention effectively:

- application logic
- API or contract changes
- database or schema changes
- auth or permissions
- configuration or infrastructure
- tests
- documentation
- dependency updates

Look for files that deserve extra scrutiny:

- auth, billing, payments, persistence, migrations, queues, background jobs
- public API contracts, DTOs, schemas, serializers
- concurrency-sensitive or caching code
- error handling and retry logic
- feature flags or rollout controls

### Hand off the deep passes

You are the generalist. When the diff touches one of these surfaces, report the
concrete risk you can see in the diff and then say the area still needs a dedicated
review — do not attempt the exhaustive audit yourself:

| Changed surface                              | Flag it, then hand off to |
| -------------------------------------------- | ------------------------- |
| auth, permissions, sessions, tokens          | `review-auth`             |
| schema migrations                            | `review-migration`        |
| database queries                             | `check-query-safety`      |
| endpoints, routes, list envelopes, DTOs      | `review-api`              |
| components, styles, keyboard, motion         | `review-ui`               |
| logging, errors, request ids, health         | `review-observability`    |
| credentials or secrets appearing in the diff | `audit-secrets`           |

The handoff is part of the finding, not a substitute for it. "Auth changed, get it
reviewed" is not a finding; "GET requests now skip the 401 check entirely — this
needs a dedicated auth review" is.

---

## Step 4 — Review for high-severity issues first

Search for the highest-risk classes of problems before anything else:

- bugs that can break the primary flow
- missing null/undefined handling
- incorrect edge-case behavior
- stale assumptions after a refactor
- schema or migration risks
- auth bypasses or permission regressions
- secrets or sensitive logging
- broken error handling or swallowed failures
- performance regressions from N+1 queries, repeated calls, or large loops
- broken backward compatibility for APIs, events, configs, or CLI flags

Ask:

- What can fail in production?
- What changed behavior without corresponding validation?
- What paths are now untested?
- What rollback risk exists if this ships?

---

## Step 5 — Check tests and verification evidence

Inspect whether the change is verified well enough:

- Were relevant tests added or updated?
- Do tests actually cover the changed behavior?
- Is there a mismatch between risk and testing depth?
- Are there manual verification notes or commands?

Do not assume tests are sufficient just because test files changed.

If verification is weak, call it out explicitly as a finding or risk.

---

## Step 6 — Produce findings-first output

Your response must start with findings, ordered by severity.

For each finding include:

- severity: high, medium, or low
- the impacted file or code area
- what the issue is
- why it matters
- what scenario triggers it

Use this structure:

```text
1. [high] <short title> — `path/to/file`
   Explain the issue, impact, and triggering scenario.
```

Rules:

- Prefer fewer strong findings over many weak nits
- If something is uncertain, state the assumption clearly
- Separate bugs from style opinions
- Mention missing tests only when it materially increases risk

If you find no significant issues, say so explicitly and then note residual risks or testing gaps.

---

## Step 7 — End with concise secondary sections

After findings, optionally include:

- open questions or assumptions
- residual risks
- brief change summary

Keep these sections short. Findings are the main deliverable.
