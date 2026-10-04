---
name: ship
description: Takes an approved plan from docs/plans/ and drives it to an open PR. Implements it by milestones, commits per milestone in the repo's style, and opens the PR against the repo's base branch. Use whenever the user approves a plan, says "ship it", "go", "start", "implement it", "do it", or asks to open a PR for already-planned work — or in Spanish "dale", "arrancá", "implementalo", "hacelo".
---

# Implement and open the PR

Takes a plan from `docs/plans/{{ticket}}.md` and drives it to an open PR.

**Precondition:** the plan exists, is approved, and has no open decisions. If there's no
plan, don't improvise: run the `plan` skill first.

Read the repo's `CLAUDE.md` before anything: the **base branch**, the **branch-naming**
convention, and the **commit format** all come from its "Git and PRs" section. Don't assume
`main`/`master`/`test` — read which one this repo uses. Resolve the GitHub repo once:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # -> {{owner}}/{{repo}}
```

## 1. Prepare

```bash
git fetch origin
git switch -c {{type}}/{{ticket}}-{{slug}} origin/{{base}}
```

`{{base}}` is the base branch from `CLAUDE.md`. `{{type}}` (`feature`/`fix`/`chore`) comes
from the nature of the ticket. `{{slug}}` is short, lowercase, hyphenated.

Reread the whole plan before writing the first line of code.

## 2. Implement step by step

For **each** step of the plan, in order:

1. Implement just that step.
2. Run lint and unit tests (commands in `CLAUDE.md`).
3. If something fails, fix it before moving on. Don't accumulate debt between steps.
4. Commit using the repo's commit format (`CLAUDE.md`), referencing the ticket.

Rules:

- **Don't go out of the plan's scope.** If ugly code or an adjacent bug shows up, note it for
  the PR's "Notes" section; don't fix it.
- If during implementation you find the plan was wrong: **stop**, update
  `docs/plans/{{ticket}}.md` with the change of approach and its reason, tell the user, and
  only then continue. Don't drift silently.
- The plan's tests get written, not left for later.

## 3. Pre-PR check

- Full test suite green.
- Lint clean.
- `git diff origin/{{base}} --stat` — check nothing extra slipped in (local config, `.env`,
  build artifacts, `settings.local.json`).
- No secrets, tokens, credentials, or internal endpoints hardcoded in the diff.

## 4. Open the PR

```bash
git push -u origin HEAD
gh pr create --base {{base}} --title "{{ticket}}: {{title}}" --body-file {{temp file}}
```

PR body:

```markdown
## What it does
{{Two or three lines.}}

## Plan
docs/plans/{{TICKET}}.md

## How to test it
{{Concrete steps to verify by hand.}}

## Notes for the reviewer
{{Non-obvious decisions. Things left out of scope on purpose. If the plan had risks, repeat
them here.}}
```

If the plan was flagged as requiring human review, or the change touches anything on the
"Changes that require human review" section of the repo's `CLAUDE.md`:

```bash
gh pr edit {{n}} --add-label "needs-human"
```

and say so in the final message.

**Always request Copilot's review**, regardless of whether the PR is `needs-human`. They're
two different things: the label is about who can merge, Copilot's review is an automatic pass
that goes either way. If it doesn't self-request:

```bash
PRID=$(gh api graphql -f query='query { repository(owner:"{{owner}}", name:"{{repo}}") { pullRequest(number:{{n}}) { id } } }' --jq '.data.repository.pullRequest.id')
gh api graphql -f query="mutation { requestReviews(input:{pullRequestId:\"$PRID\", botIds:[\"BOT_kgDOCnlnWA\"], union:true}) { clientMutationId } }"
```

(`BOT_kgDOCnlnWA` is `copilot-pull-request-reviewer` — a single global GitHub App id, stable
across repos. The REST `requested_reviewers` API rejects it with 422 because it's not a
collaborator; go through GraphQL with `botIds`.)

## 5. Close

Return **only** the PR URL and one line about what's left for human review, if anything.
Don't summarize all the work: the user sees it in the PR.

Then **invoke the `watch` skill** with the PR number, in the same turn and without asking for
confirmation. The session stays watching the review. **No exceptions**: a `needs-human` PR
also goes through the watcher. The label stops the merge, not the review.

Never merge. The merge to the base branch is always done by a person.

---

*Convention: `{{like-this}}` marks a value to replace. `<>` is avoided because it breaks skill parsing.*
