---
name: fix
description: Processes a PR's review comments (Copilot or human), classifies them, applies the fixes that belong, replies to each thread, and pushes. Use whenever the user says "address the review", "fix what Copilot said", "handle the comments", mentions Copilot already reviewed a PR, or passes a PR number/URL with pending reviews — or in Spanish "revisá los comentarios", "arreglá lo que dijo Copilot", "atendé el review".
---

# Address review comments

Turn a PR's comments into commits or into justified replies. **Two automatic rounds max**;
the third is for a human.

Resolve the repo once up front; every `gh` call below uses it:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # -> {{owner}}/{{repo}}
```

## 1. Determine the round

```bash
gh pr view {{n}} --json labels,title,url
```

- No `ai-round-*` label -> this is **round 1**.
- Has `ai-round-1` -> this is **round 2**.
- Has `ai-round-2` -> **STOP**. Don't touch code. Go straight to step 5 (escalate).

The `needs-human` label does **not** stop this skill: it means a human does the merge, not
that comments go unaddressed. Both Copilot rounds run anyway. The only things that stop the
rounds are `ai-round-2`, or a comment landing in the "Human" group (step 3).

## 2. Pull the unresolved comments

```bash
gh pr view {{n}} --comments
gh api repos/{{owner}}/{{repo}}/pulls/{{n}}/comments --paginate
```

Discard threads already resolved and comments already answered in earlier rounds. Copilot
tends to repeat comments that were already dismissed: if a previous thread has a justified
rejection, don't reopen it.

Make sure you're on the PR branch and up to date:

```bash
git switch {{pr-branch}} && git pull
```

## 3. Classify each comment

Before touching anything, classify **all** comments into three groups and show the user the
classification:

| Group | Criterion | Action |
|---|---|---|
| **Accept** | Real bug, concrete risk, or a `CLAUDE.md` convention broken | Fix it |
| **Reject** | False positive, generic style suggestion that contradicts `CLAUDE.md`, or out-of-scope refactor | Reply to the thread with the reason, don't touch code |
| **Human** | Touches something on the "Changes that require human review" list, or implies a design decision the plan didn't make | Don't touch. Goes to step 5 |

Core criterion: **a comment is not an order**. Rejecting with an argument is a valid response
and preferable to a mechanical fix that dirties the diff.

## 4. Apply and reply

For the "Accept" group:
- Fix it. One commit per topic, not one "fix review comments" commit with everything in it.
- Run lint and tests after each fix.
- Reply to the thread saying what changed and in which commit.

For the "Reject" group:
- Reply to the thread with the concrete reason. No bare "doesn't apply".

```bash
gh api repos/{{owner}}/{{repo}}/pulls/comments/{{comment_id}}/replies -f body="{{reply}}"
```

Then:

```bash
git push
gh pr edit {{n}} --add-label "ai-round-{{N}}" --remove-label "ai-round-{{N-1}}"
```

## 5. Escalate what doesn't resolve itself

If there are "Human" group comments, or this was round 3:

```bash
gh pr edit {{n}} --add-label "needs-human" --add-assignee "@me"
```

And leave **one** comment on the PR with the status:

```markdown
## Pending human review

- [ ] {{comment/topic}} — {{why it needs a human decision}}

Automatic rounds completed: {{N}}/2
Auto-resolved this round: {{count}} fixes, {{count}} justified rejections.
```

## 6. Close

Report to the user in three lines: how many were fixed, how many rejected and why, and what's
left for them. If nothing is pending and the PR is green, say so explicitly — that's the
signal they can merge.

Never merge.

---

*Convention: `{{like-this}}` marks a value to replace. `<>` is avoided because it breaks skill parsing.*
