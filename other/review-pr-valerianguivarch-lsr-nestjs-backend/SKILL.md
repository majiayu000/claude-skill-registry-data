---
name: review-pr
description: >
  Reviews a GitHub Pull Request and posts structured feedback as a GitHub review.
  Use this skill whenever a user wants to review, comment, or give feedback on a PR.
  Trigger on: "review cette PR", "commente la PR", "reveille la PR #123", "donne du feedback sur la PR",
  "qu'est-ce que tu penses de cette PR ?", "review la PR de [nom]", "analyse les changements de la PR",
  "check la PR", "fais une review".
  Requires GitHub MCP to be configured. Use Jira MCP to validate PR content against ticket intent.
---

## Purpose

Produce a thorough, actionable code review of a Pull Request, and post it as a GitHub review.
Each finding is posted as an **inline comment** on the relevant line. The general review body is
reserved for a short closing summary only.
When a Jira ticket is linked, validate the PR against the ticket's acceptance criteria and Definition of Done.

## Inputs to collect

Before reviewing, gather:

1. PR identifier — accept any of: a PR number (`#NNN`), a PR URL, or a branch name. If a branch name is given, use `list_pull_requests` with `head=<branch>` to resolve the PR number. Ask the user only if none of these can be inferred.
2. Optional: Jira ticket key — infer from PR title if it matches `IDF-XXXX:...`; fetch from MCP if available

## GitHub repository

This project is always hosted at:

- **owner**: `faberNovel`
- **repo**: `idf-subventionjeunes-web`

Use these values for all GitHub MCP calls. Never guess or ask the user.

## Step 1 — Fetch PR data

Via GitHub MCP:

- `get_pull_request` — title, description, author, base branch, state
- `get_pull_request_files` — full list of changed files with patches

If a Jira ticket key is found, also fetch via Jira MCP:

- `fields=summary,description,customfield_12948,customfield_12947,customfield_12946`

## Step 2 — Analyse the changes

### 2a — Read the coding standards

Before evaluating any finding, read the coding standards — they are the source of truth:

- `apps/idf-young-documentation/docs/coding-standards/architecture.md` — layer conventions, domain/api/ui separation, framework-free domain rule
- `apps/idf-young-documentation/docs/coding-standards/result-pattern.md` — error-handling expectations in services and repositories
- `apps/idf-young-documentation/docs/coding-standards/naming-conventions.md` — file, class, and method naming

### 2b — Mini debt-radar on the diff

For every file in the diff, check the following signals. These are architecture violations that
must never be introduced, regardless of how common they are elsewhere in the codebase.

| Signal                      | Files to check             | Violation                                              |
| --------------------------- | -------------------------- | ------------------------------------------------------ |
| `import.*@nestjs/swagger`   | `*-domain/**/*.ts`         | Framework dep in domain layer                          |
| `import.*class-validator`   | `*-domain/**/*.ts`         | Framework dep in domain layer                          |
| `import.*class-transformer` | `*-domain/**/*.ts`         | Framework dep in domain layer                          |
| `import.*@nestjs/common`    | `*-domain/**/*.ts`         | Framework dep in domain layer                          |
| `@ApiProperty` on errors    | `*-domain/src/errors/*.ts` | Swagger decorator on a domain error                    |
| Files named `*.view.ts`     | `*-domain/src/`            | View in domain — should be in `*-api/src/views/`       |
| Files named `*.query.ts`    | `*-domain/src/`            | Query in domain — should be in `*-api/src/queries/`    |
| Files named `*.command.ts`  | `*-domain/src/`            | Command in domain — should be in `*-api/src/commands/` |

Any signal found in a **newly added or modified** file is a **Must** finding.

### 2c — General code analysis

Go through each changed file and reason about:

- **Correctness** — does the code do what it says? are there edge cases or bugs?
- **Tests** — are meaningful tests added? are edge cases covered?
- **Style** — does the code follow the project conventions (TypeScript, NestJS, Next.js patterns)?
- **Migrations** — if data model changes are present, are migrations generated and committed?
- **Security / RGPD** — any personal data exposure or missing access control?
- **Documentation** — any public API or config change that requires a doc update?

### 2d — Classify findings with MoSCoW

- **Must** — blocks the merge; the PR cannot be approved without this fix
- **Should** — strongly recommended but not a blocker
- **Could** — a nice improvement, optional
- **Won't** — out of scope; never raise it

Only surface Must, Should, and Could items. Never raise Won't items.

## Step 3 — Check against the PR template

Verify that the PR description covers:

- A clear description of what changed and why
- Breaking changes section filled in honestly
- Coding checklist: style, docs, migrations, tests
- Project checklist: Keycloak, Notion, PR dependencies

If sections are missing or incomplete, flag them as a finding (typically **Should**).

## Step 4 — Check against the Jira ticket (if available)

When a ticket was fetched:

- Go through each acceptance criterion → is it implemented?
- Go through the Definition of Done → is each item met?
- Go through Identified Tasks → are all tasks reflected in the code?

Coverage output format:

- ✅ Implemented
- ⚠️ Partially implemented or unclear
- ❌ Not implemented

## Step 5 — Present all findings to the user, then post one by one

### 5a — Present the full list and let the user curate it

Before posting anything, show the user a summary of all findings ordered: Must first, then Should,
then Could. For each finding, show: MoSCoW level, target file, line, and a one-line description.

The user may approve, reject, or adjust each finding. Wait for an explicit go-ahead on the full
list before moving to 5b. Do not post anything yet.

### 5b — Post each approved finding one by one, with explicit confirmation before each post

For each approved finding, in MoSCoW order, repeat this exact loop:

1. Show the user the **exact text that will be posted on GitHub** — nothing more, nothing less
2. Wait for explicit confirmation ("go", "oui", or equivalent)
3. Only then post it via `create_pull_request_review` with:
   - `event: COMMENT`
   - `body: ""` (empty — no general body)
   - a single inline comment using the parameters below
4. Move to the next finding

#### Inline comment line targeting

**Always use `line` + `side` — never compute a `position` manually.**

- `line`: the **absolute line number** in the file (same number you would see in the GitHub
  file view or in your editor). Read it from the `patch` field of `get_pull_request_files`:
  start from the first line referenced in the `@@ -A,B +C,D @@` header (value `C` is the
  starting line in the new file) and increment for each `+` or context line.
- `side`: `"RIGHT"` for added or context lines (new version of the file); `"LEFT"` for
  deleted lines (old version of the file). Use `"RIGHT"` in the vast majority of cases.

**Why not `position`?** The `position` parameter is a diff-relative offset (1 = the `@@` header
line itself, then +1 per diff line regardless of type). It is error-prone to compute and causes
comments to land on wrong lines. The `line` + `side` approach uses absolute file line numbers
and is reliable.

If the GitHub MCP tool only accepts `position` and does not support `line`/`side`, compute it
as follows: walk the `patch` string from top to bottom; the `@@ ... @@` header = position 1;
each subsequent line (context, `+`, `-`) increments the counter by 1. The `position` for a
finding on line N (right side) is the index of that `+` or context line in this sequence.

Never batch-post multiple comments. Each comment is shown, confirmed, and posted individually.

**Inline comment template:**

```
**[Must]** <concise description of the problem>

Fix: (if applicable)
<code block>
```

Replace `Must` with `Should` or `Could` as appropriate.

### 5c — Post the closing review

Once all inline comments are validated and posted, post the closing review via `create_pull_request_review`:

- `event`: `REQUEST_CHANGES` if any Must items, `APPROVE` if none, `COMMENT` if the user asked for no verdict
- `body`: short closing summary using this template:

```
## Summary
[2–3 sentences: overall assessment, key strengths, key blockers if any]

## Ticket coverage
[acceptance criteria and DoD table — ✅ / ⚠️ / ❌]

## What's well done
[at least one positive item — never skip this]
```

## Step 6 — Optional Slack notification

Once the full review is posted on GitHub, ask the user:

> "Veux-tu prévenir la personne sur idf-dev ?"

- If **yes**: ask for the Slack handle to tag (e.g. `@jean.dupont`), then follow the `slack-notify` skill (`.claude/skills/slack-notify/SKILL.md`) — use the **"PR review notification"** template defined there.
- If **no**: skip silently.

Never post to Slack without explicit confirmation.

---

## Rules

- **Never put findings in the general review body.** All findings (Must/Should/Could) are inline comments on the relevant lines.
- Always show each comment to the user and wait for validation before posting.
- Never approve a PR with Must findings.
- Do not invent defects — only flag things that are actually present in the diff.
- Write all review comments and the review body in English.
- If the GitHub MCP is unavailable, provide the review as text for the user to post manually.
