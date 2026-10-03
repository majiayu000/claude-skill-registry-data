---
name: code-review-judge
description: Decide with the user which review findings to fix
disable-model-invocation: true
---

# Code Review Judge

Discuss each code-review finding with the user in this session. The general framework:

1. Identify the review scope: working tree, commit, branch, pull request, or path.
2. If scope is unknown or missing, ask the user.
3. Log the scope and current HEAD SHA at the top of the decision log.

**Start a decision log** in a scratch file outside the repository. It should contain the full
original context of every finding, including its source — the finder, agent, or reviewer that
reported it — when the review names one. A long walk can outlive the context window; the log is
what survives. Write each decision as soon as it is made.

**Use plain words.** Write for an average developer who has not seen this codebase. Do not use
jargon that only a narrow field or one language community knows. If the findings need a few key
terms, define them in a short glossary before the first finding, copy it into the decision log, and
use only those terms.

For each finding:

- Describe the conditions under which it happens, and rate their **likelihood**.
- Describe its impact, and rate the **impact**.
- Give one concrete example of the bad case: the input, state, or sequence of events, and what the
  user, the data, or the system ends up with.
- Describe what the fix would look like.
- Replay the same example with the fix in place, and show what happens instead.
- Rate the **fix cost**.
- Rate the **architecture friction** of the fix.
- Summarize.
- Recommend one option, with a one-line reason.
- Ask the user to decide. Offer these options:
  - **Fix** — when there are several ways, list them.
  - **Defer** — an issue for later. Record only where it goes: a kotgent task, Jira, or GitHub. The
    plan creates it; for kotgent, through `kotgent:create-tasks`.
  - **Do nothing** — record why: false positive, won't fix, or accepted risk.
  - **Dig deeper** — discuss the finding with the user, then ask again.
- Do not move on without an answer.

Each rating is 1–5, and 5 means more of what the name says:

| Rating | 1 | 3| 5|
|---|---|---|---|
| Likelihood | needs an unusual mix of input, state, or timing | needs a specific but ordinary condition: a setting, a retry, a concurrent call | happens easily and often in normal use |
| Impact | cosmetic, or recovers by itself | a feature is wrong or down until someone fixes it by hand | loss of data or reputation that cannot be undone |
| Fix cost | a local one-line change | several files or new test setup within one module | a redesign across modules, or a migration |
| Architecture friction | uses existing patterns as they are | needs a new helper or a small exception to a pattern | breaks the architecture, or needs it changed first |

High likelihood and impact argue for fixing; high fix cost and friction argue against.

Based on the answers for all findings, propose a plan that carries them out:
- Sequential or parallel.
- Separate commits or a single commit, and whether to amend when the review covered a single commit.
- Which deferred issues to create, and where.

Safety Policy:
- Never rewrite remote history without explicit user approval.
- If a plan requires amending pushed commits or 'git push --force-with-lease', obtain specific approval first.
- On the default branch, only use new commits.
- If approval is withheld, use new commits and do not push.

Store the plan in the scratchpad. It must contain the glossary, the full context of the findings,
and the decisions the user made. Print the absolute path to the plan, and suggest clearing the
context and running it.
