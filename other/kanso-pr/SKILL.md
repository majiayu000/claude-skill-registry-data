---
name: kanso-pr
description: Use when the user asks to write a pull request description, open a PR, draft PR notes, or summarise a branch for review.
argument-hint: "[optional: target branch, defaults to main]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(gh pr *) Bash(gh repo *)
---

# kanso-pr

Writes PR descriptions that survive Jira migrations, Slack thread rot, and six months of organisational drift. Self-contained by default. Pulls from commit history rather than re-inventing.

The principles from `kanso-principles` apply. The description earns its place the same way code does.

## The job

A PR description has two readers: the present reviewer and the future archaeologist. The present reviewer needs enough context to approve or push back. The future archaeologist — human or AI — needs enough context to understand *why* without cloning the repo, reading the diff, and reverse-engineering intent.

External links rot. The description must stand on its own. Links supplement; they don't substitute.

## Before writing

Gather context in this order:

1. **Target branch.** `!git rev-parse --abbrev-ref HEAD` for current, `$ARGUMENTS` or `main` as target.
2. **Commit history on this branch.** `!git log <target>...HEAD --format="%h %s%n%b%n---"`. These commits already contain the *what* and ideally the *why*. Pull from them.
3. **Diff summary.** `!git diff <target>...HEAD --stat` for scope awareness.
4. **Recent merged PRs for voice calibration.** `!gh pr list --state merged --limit 5 --json title,body` (if `gh` is available). Match the tone and structure of what the repo already merges.
5. **PR template.** `!find . -path '*/PULL_REQUEST_TEMPLATE*' -o -name 'pull_request_template*'`. If one exists, use it as the skeleton instead of the default.

If no PR template exists and no recent PRs are findable, fall back to the universal skeleton below.

## The universal skeleton

```markdown
## What

<One or two sentences. What does this PR accomplish? Must be
independently meaningful — not "see title".>

## Why

<The problem being solved. What broke, what was slow, what was
impossible that should be possible. Include the impact of NOT making
this change if it's relevant.>

## How (non-obvious decisions only)

<Skip this section entirely if everything in the diff is self-evident.
Otherwise: algorithmic choices, data structure decisions, architectural
tradeoffs that aren't visible in the code. One bullet per decision.>

## Verification

<What was actually run and the result. Test command and outcome,
typecheck, lint, manual paths exercised. If something wasn't tested,
say so explicitly and why — "no integration tests exist for this
module" beats silence. Reviewers shouldn't have to guess what's
covered.>

## Risks

<Side effects, performance implications, known limitations, anything
intentionally NOT changed. Rollback plan if non-obvious.>

## References

<Issue numbers, design docs, related PRs. Short list, not a dump.>
```

Sections that have nothing to say are omitted, not padded. A PR that doesn't need a "Risks" section shouldn't have an empty one.

## Pulling from commit history

If the branch has well-written commits (ideally via `/kanso-commit`), the PR body is mostly synthesis rather than invention:

- **What** → subject lines of the commits, combined.
- **Why** → bodies of the commits, deduplicated and organised.
- **How** → any non-obvious decisions already in commit bodies.
- **Verification** → any test-related commits, whatever's new in `__tests__/` or `*.test.*` files, plus the verify results from `/kanso-audit` or `/kanso-refactor` if they ran on this branch.

If commits are poorly written ("fix", "wip", "more work"), the PR body has to carry all the context that the commits lack. Flag this to the user — ideally they should rewrite the commits before opening the PR, or at least squash on merge.

## Size-proportional depth

A 50-line PR doesn't need a five-section description. A 2,000-line PR needs more context, not less — counterintuitively, large PRs often have the shortest descriptions because authors assume the scope speaks for itself. It doesn't.

Rule of thumb:

- Under 50 lines: What + Why, single paragraph each. Often no other sections.
- 50-300 lines: Full skeleton, concise.
- Over 300 lines: Full skeleton, with narrative structure. Start with "Where to start reading" pointing reviewers at the most important file. Consider whether the PR should be split.

If the diff is over 500 lines and touches more than a few concerns, recommend splitting before writing the description.

## Stacked or split PRs

If this is part of a series, the description must say so:

```
This is PR 2 of 4 in the feature X series.

- PR 1 (#123, merged): schema migration and API stubs
- PR 2 (this): core logic for X
- PR 3 (#125, open): edge cases and error handling
- PR 4 (not yet opened): documentation and metrics

This PR intentionally does not include <what's deferred to PR 3/4>.
```

Each PR in a series should be reviewable in isolation. If it isn't, the split is wrong.

## The "why" cannot be generated

This is the core limitation worth stating plainly. AI-generated PR descriptions are consistently good at the *what* (summarising the diff) and consistently weak at the *why* (which lives outside the codebase: business context, prior decisions, regulatory constraints, conversations that happened elsewhere).

If the user hasn't explained why the change is needed, and the commits don't contain it, ask before writing the PR. Options:

- "The commits don't explain why this change is needed. Can you give me the motivation?"
- "Is this tied to an issue I should reference?"
- "Was there a prior approach that was rejected? If so, why?"

Don't invent a plausible-sounding *why*. An invented rationale is worse than a missing one.

## Breaking changes and migrations

If the PR introduces a breaking change:

- Call it out at the top, not buried in "Risks".
- Include a migration path: concrete before/after code examples.
- Reference the deprecation timeline if one was promised.

Example:

```markdown
## ⚠️ Breaking change

The `/api/users` endpoint now requires a `x-client-version` header.
Requests without it will receive a 400 response.

Migration:

Before:
GET /api/users

After:
GET /api/users
x-client-version: 2.0
```

## Tone

Match recent merged PRs in the repo. Some teams are terse and imperative. Some are conversational. Some use emoji headers. The description should look like it belongs.

General rules regardless of tone:

- No filler. "This PR does X" → just "X".
- No hedging. "I think this might possibly..." → state it.
- No apology. "Sorry this is large" adds nothing.
- No AI artefacts. No "I've implemented", no "Let me know if any changes are needed", no "Hope this helps".

## Working process

1. Detect target branch and fetch commit history on this branch.
2. Check for a PR template and recent merged PRs for voice.
3. Draft the sections from commit content + the user's intent.
4. If the *why* is missing from both commits and the user's prompt, ask.
5. Show the draft to the user before opening the PR.
6. On approval, use `gh pr create` to open the PR (or print the body if `gh` isn't available).
7. Report the PR URL.

## Output format

Show the user:

```
Target: main ← feature/oauth-refactor (12 commits, +340 -180)

Draft PR description:

---

## What

Replace the legacy OAuth implementation with PKCE-based flow.

## Why

The previous implicit grant flow is deprecated by RFC 8252 for SPA
clients due to token leakage via browser history. PKCE adds a
per-request secret that makes interception attacks infeasible.

...

---

Open the PR? (y/n/edit)
```

Wait for approval before running `gh pr create`.

## What this skill never does

- Open a PR without showing the description for approval first.
- Invent motivation or context the user didn't provide.
- Include AI attribution in the body ("Written by Claude", "AI-assisted") unless the user asks.
- Use the default GitHub title. The title is the most important line; draft it.
- Copy the entire diff into the body.
- Write a description longer than the diff it describes.
- Open a draft PR as a non-draft or vice versa without asking.

## Failure modes to avoid

- Descriptions that just link to Jira and say nothing else.
- Descriptions that recap the diff line by line.
- Descriptions that start with "This PR" (redundant — of course it does).
- Overly formal corporate prose on a repo that's historically casual, or vice versa.
- Missing the *why* entirely because it wasn't in the commits and you didn't ask.
- Sections padded with "N/A" or "None" instead of being omitted.
