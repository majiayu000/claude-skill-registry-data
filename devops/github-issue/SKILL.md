---
name: github-issue
description: Draft and file a GitHub issue with the shape that fits its kind — task (user story + acceptance criteria), bug (repro steps + expected/actual), or spike (decision + question). Use when asked to open, file, or create a GitHub issue.
---

# Creating a GitHub issue

Three kinds, three body shapes. `gh issue create` does the actual filing once the body and label
are drafted.

## 0. Don't read the repo

The user's request is almost always enough on its own — as much context as a ticket would need
from a human. Draft straight from what they said; don't `Read`, `Grep`, or spawn an agent to go
looking through the codebase first. If you genuinely can't draft without seeing something specific
(a file, a script, a config), ask the user before reading it rather than reading on your own
judgment. Reading is the exception here, not the default.

## 1. Pick the kind

Ask if it isn't obvious from the request — the wrong pick produces a body with dead sections
(acceptance criteria on a bug, repro steps on a task).

| Kind | When | Label |
| --- | --- | --- |
| Task | A regular unit of work — no bug, no open question | `enhancement` |
| Bug | Something that works today works incorrectly | `bug` |
| Spike | A decision has to get made before work can start | `spike` (+ `question` if it's a genuinely open call, e.g. #26) |

Check `gh label list` if a label looks stale — the mapping above is what this repo's tracker uses
today, not a guarantee it always will.

## 2. Pick the area and the board

Every issue also gets one **area label**, which says which folder the work lives in:
`app:<name>`, `package:<name>` or `infra:<name>`, or `repo` for work that spans the whole repo
(CI, docs, conventions). The kind label from step 1 sits next to it. Deployment and pipeline work
for an app takes that app's label, not `repo`. Ask if the folder isn't obvious from the request.

There is one board, `Joinery`, and every issue goes on it: pass it through to `gh issue create`
(step 4) so the issue actually lands there instead of just existing in the repo. A finite effort,
such as a launch, is a milestone, not a board.

## 3. The templates

### Task

Title: short imperative, sentence case, no trailing period — "Develop contact view", not
"Developing the contact view.".

```markdown
**User story:** As a <role>, I want <capability>, so that <benefit>.

**Acceptance criteria:**
- [ ] <criterion>
- [ ] <criterion>

**Blocked by:** #<n>
```

Drop the `Blocked by` line entirely if nothing blocks it — don't leave it empty.

### Bug

Title: the symptom, not the fix — "Contact form submits twice", not "Fix double form submit".

```markdown
**Description:** <what's broken and where, one or two sentences>

**Steps to reproduce:**
1. <step>
2. <step>

**Expected behaviour:** <what should happen>

**Actual behaviour:** <what happens instead>
```

### Spike

Modeled on the one spike already in this tracker (#26) — a decision, framed as a real choice, plus
what's waiting on it:

```markdown
**Decision needed.** <context: what's planned or assumed, and what it's in tension with>

**Question:** <the actual question, framed as a choice between named options>

**Blocks:** <the work waiting on this decision, or "nothing yet">
```

## 4. File it

Show the drafted title, body, label and project to the user before running this — filing an issue
is outward-facing (it notifies watchers) even though it's easy to edit or close after the fact:

```sh
gh issue create --title "<title>" --body "<body>" --label "<kind>" --label "<area>" --project "Joinery"
```

Drop `--project` only if the user says so.
Add `--milestone "<name>"` only if the user names one — don't invent a milestone. Report back the
issue number and URL `gh issue create` prints, not just "done".

## 5. Offer to pick it

Once it's filed, ask whether the user also wants to pick it up now. If yes, run the same script
they would, with the number so it asks nothing:

```sh
pnpm issue:pick <issue number>
```

It takes the branch's middle segment from the area label and the branch type from the kind label:
`enhancement` is `feature`, `bug` is `fix`. It fails rather than guessing for a `spike`, and the
message names the flag to pass — `--type=<feature|fix|hotfix|release>`; ask the user if it isn't
obvious. Pass a short
`--title="…"` when the issue title would make a long slug. A failed assignment or board move only
warns; the branch is still checked out.
