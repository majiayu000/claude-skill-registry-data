---
name: padosoft-pr-review-triage
description: >-
  Use this skill when a pull request has comments from an automated reviewer — GitHub Copilot, Codex,
  CodeRabbit, Advanced Security — and the user wants them processed: "copilot review", "the bot comments on
  the PR", "address the review", "fix the Codex findings", or simply "there are 14 comments on PR 212, sort
  them out". It reads every bot comment, sorts them into must-fix / worth-fixing / negligible / bot-is-wrong,
  gets the categorisation approved before touching code, applies only the approved fixes, replies to each
  comment on GitHub, and proposes a new project rule when the bot found a real bug the project checks would
  have missed. Do not use it for a human reviewer's comments, for a single comment, or to write the code
  review itself.
license: MIT
compatibility: >-
  GitHub repositories. Requires the `gh` CLI, authenticated with access to the repository (`gh auth status`).
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A bot review is a list of candidates, not a task list.
  profiles: devops
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: pull request, code review, copilot, codex, coderabbit, github, gh cli, triage
---

# PR review triage

A bot review is a list of *candidates*, not a task list. Applying all of it produces changes nobody asked
for; ignoring all of it loses the real bugs. This skill separates the two, with the user deciding in the
middle.

**The rule that makes it work: never touch code before the categorisation is approved.**

---

## 1. Collect

| Item | How |
|---|---|
| PR number | Ask, if not given |
| Repository | `gh repo view --json nameWithOwner --jq '.nameWithOwner'` |
| Current branch | `git branch --show-current` — confirm it is the PR's branch |

```bash
# inline review comments
gh api repos/{owner}/{repo}/pulls/{PR}/comments --jq '
  [.[] | {id, user: .user.login, type: .user.type, path, line, body, in_reply_to_id}]'

# general PR comments
gh pr view {PR} --json comments
```

Bots post under several logins — `copilot`, `copilot-pull-request-reviewer[bot]`,
`github-advanced-security[bot]`, `chatgpt-codex-connector[bot]`, `coderabbitai[bot]`. **Do not filter on one
name.** Take everything where `user.type == "Bot"`, then decide by content. Missing a comment is worse than
reading one too many.

Read the **whole thread**: a comment with `in_reply_to_id` may already be answered or superseded.

### Getting the complete set, which is harder than it looks

- **Paginate to exhaustion.** A threads query without following the page cursor silently returns the first
  page and nothing else, so actionable threads beyond it never reach you. Over REST the same applies:
  without pagination you can miss the review for the current head — and note that a paginated call may emit
  **one document per page**, which is not valid to parse as a single value.
- **`commit_id` can move.** When a comment is successfully repositioned onto a newer diff, that field is
  updated; `original_commit_id` still identifies the SHA where the finding was raised. Use the original when
  you need to know *what* was being reviewed.
- **Keep mutations and verification separate**, check the API's exit code before dereferencing the response,
  and then **re-query the authoritative state**. A mutation that reported success and a follow-up count read
  from a null response look identical in a log.

## 2. Categorise

| Category | Criterion | Action |
|---|---|---|
| 🔴 **Must fix** | Real bug, crash, security issue, wrong logic, race condition | Fix |
| 🟡 **Worth fixing** | Performance, readability, a sensible refactor, a good practice the project has no rule about | Fix if approved |
| ⚪ **Negligible** | Minor style, cosmetics, subjective naming | Skip, reply briefly |
| 🚫 **Bot is wrong** | The pattern is correct *for this project*, or the suggested fix does not apply | Reply with the reason |

A bot is typically wrong when it: suggests a pattern that **contradicts a project convention** (cite the
rule); re-adds handling the caller or parent already does; asks for a `try/catch` where errors are handled a
level up; or asks for a type that the compiler already infers.

Present it and **stop**:

```markdown
## Bot comments on PR #{n} — categorisation

### 🔴 Must fix ({n})
1. **{file}:{line}** — {what the bot says}
   → FIX: {what to do}

### 🟡 Worth fixing ({n})
### ⚪ Negligible ({n})    → REASON: {why}
### 🚫 Bot is wrong ({n})  → REASON: {the project rule it contradicts, or why it does not apply}

---
What do you want to do?
- [ ] Must fix + worth fixing
- [ ] Must fix only
- [ ] Everything, negligible included
- [ ] Custom (say which numbers)
```

## 3. Fix

For each approved comment:

1. **Read the whole file first.** A fix applied to a diff hunk in isolation breaks the surrounding context.
2. **Check the suggestion against the project conventions.** If the bot's version violates them, apply the
   version that is *correct for the project*, not the one it wrote — and say so in the reply.
3. Apply the edit.
4. **Check shared code.** If the change touches a shared package or module, verify the other consumers still
   build.

## 4. Commit and push

One commit per logical group, not one per comment — bot comments cluster on the same file.

```bash
git add {files}
git commit -m "fix: address review comments on PR #{n}

- {fix 1}
- {fix 2}"
git push origin $(git branch --show-current)
```

## 5. Reply to every comment

Every processed comment gets a reply, including the ones you did not act on. A silent thread is re-raised by
the next reviewer.

```bash
gh api repos/{owner}/{repo}/pulls/{PR}/comments \
  -X POST -F in_reply_to_id={comment_id} \
  -f body="Fixed in {short_sha}. {one line on what changed}."
```

| Category | Template |
|---|---|
| 🔴 fixed | `Fixed in {sha}. {what changed}.` |
| 🟡 fixed | `Good catch, fixed in {sha}. {what changed}.` |
| ⚪ skipped | `Noted — intentional here / low priority for this PR. {reason}.` |
| 🚫 wrong | `This follows our {rule}: {one-line why}. No change needed.` |

**One or two lines.** Nobody reads a paragraph from a bot thread, bots included.

## 5b. Knowing when a reviewer is done, and when it only looks done

Re-requesting a bot that has nothing new to say spends review budget and returns no signal. But "done" is
easy to misread, so check what you actually have:

- **A request event is not a review.** The platform records the request immediately and the review may arrive
  minutes later — or never. Poll for a *submitted* review, and verify the **reviewer** and the **commit SHA**
  before believing it.
- **A submitted review can contain no analysis.** A response whose body is an internal error is a review
  record with nothing in it. It is not a pass.
- **"No new comments" can still list suppressed findings.** Read the body: if it names actionable items,
  they are actionable. Fix them with tests, then treat the reviewer as terminal.
- **Track the terminal state per bot.** Once one has returned nothing new or cosmetic-only feedback, stop
  re-requesting *that one*; the others are independent.
- **An adjacent API answering "no seats" is not proof of failure.** It may not describe the reviewer's
  effective access. Proof is a submitted review on the right SHA, nothing else.

## 6. Learn from it

**Only for 🔴 comments where the bot found a legitimate bug that the project's own checks would have missed.**
That is the signal worth keeping: the bot found what your review did not.

```markdown
## Proposed new rule

Bug: {what it was}   ·   File: {path}:{line}
Why it slipped through: {the check that does not exist}

- [ ] Add a check to {the project's pre-commit/review skill}
- [ ] Add a rule to the project conventions file
- [ ] Not worth it — isolated case
```

Do **not** add a rule for every bug found: rules that are too specific dilute the ones that matter. Add one
when the pattern can recur. If you add it to the conventions file, update the skill that enforces it in the
same PR — a rule the checks do not know about is a comment, not a rule.

---

## Anti-patterns

| Anti-pattern | Why it is wrong |
|---|---|
| Applying every suggestion | The bot does not know the project conventions |
| Ignoring the whole review | Bots do find real bugs — categorise one by one |
| Fixing before approval | The user decides the scope, this is their PR |
| Fixing from the diff hunk alone | The hunk hides the context that makes the fix wrong |
| Applying the bot's patch verbatim | It may violate a project rule; apply the correct fix |
| Long replies | One or two lines |
| A new rule for every finding | Over-specific rules bury the important ones |

## Checklist

- [ ] All bot comments read, inline and general, threads included
- [ ] Every comment categorised 🔴/🟡/⚪/🚫
- [ ] Categorisation approved by the user **before** any edit
- [ ] Each fix made after reading the whole file and checked against the conventions
- [ ] Shared consumers still build
- [ ] Commit pushed to the PR branch
- [ ] Every comment answered, one or two lines
- [ ] 🔴 findings assessed for a new rule; proposed only if it can recur

## Final report

```
PR #{n} — {owner}/{repo}
Comments: {t} total → 🔴 {a}  🟡 {b}  ⚪ {c}  🚫 {d}
Applied: {n} ({which})      Commit: {sha}
Replies posted: {n}/{t}
New rule proposed: {yes, which | no}
Left open: {…}
```
