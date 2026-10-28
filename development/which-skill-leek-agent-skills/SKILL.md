---
name: which-skill
description: Not sure which skill to reach for? Name the situation and get routed to one.
disable-model-invocation: true
argument-hint: "Describe your situation"
model: sonnet
effort: low
---

# Which Skill

The user does not know which skill fits. Read their situation, then **name one skill** and say why in a sentence. Recommend, never invoke: most of the skills below are user-invoked, so only the user can start them.

If the situation is genuinely ambiguous, ask one question that separates the branches, not a menu of everything.

## The pipeline

Most work runs one straight line (**decide → spec → tickets → build**) over `.scratch/<slug>/`. Route by where the user actually is:

| They have… | They want… | Route to |
|---|---|---|
| a vague idea | it stress-tested | `grill-with-docs` (default in an existing codebase), or `grill-me` for a plain interview |
| work too big for one session | a map of the decisions | `wayfinder` |
| an open question needing sources | cited findings | `research` |
| a question only someone else can answer | a document to send them | `to-questionnaire` |
| a settled conversation | it written down | `to-spec` |
| a spec | build ticket files | `to-tickets` |
| an inbound issue or external PR | it categorised and briefed | `triage` |
| one ticket | it built end to end | `implement` |
| a spec | the whole thing built fast, in parallel, this session | `implement-spec` (`implement <spec> all` for one-by-one, no subagents) |
| a map, spec, or tickets, and no wish to babysit | it driven to done | `autopilot` |

**Before any of it, once per repo:** `setup` writes the tracker, status vocabulary, and domain doc layout.

**Steps only a human can do** (a third-party dashboard, credentials, CI secrets, a one-off cutover) → `wizard` scripts the walkthrough.

## After the code exists

- Review the diff → `code-review`. Want four independent models on it instead of one → `panel`.
- Prove it in the running app → `verify`.
- Ship the session's work → `commit`.
- Write or rewrite a PR body → `pr` (the agent also reaches for it on its own).
- Review comments waiting on a PR → `resolve-review-comments`.
- A PR to take all the way to merged (reviews, checks, fixes, merge) → `triage-github-pr`.
- Merge or rebase blocked → `resolving-merge-conflicts`.
- About to close the session and want to know what is still open → `closeout`.

## Something is wrong

- Broken, throwing, failing, or slow → `diagnosing-bugs`.
- A backlog of production or review-bot issues → `fix-nightwatch-issues`, `fix-posthog-issues`, or `fix-github-issues` for the source they come from.
- The shape of the code is the problem, not one bug → `improve-codebase-architecture` to find the opportunity, `architecture-satisfaction` to run the refactor loop, `codebase-design` for the vocabulary either one uses.
- Suspect a specific module smells → `code-smells-audit`.
- Nothing known is wrong, but you want the next unnoticed problem found, proven, and fixed as a PR → `sweep`.
- Unsure whether a state model or a UI direction holds up → `prototype`.

## Repo upkeep

`housekeeper` (low-risk cleanup), `repository-cleanup` (branches, PRs, stashes, worktrees), `scratch-cleanup` (file research, remove finished efforts, report open work in `.scratch/`), `dependency-audit` (upgrade plan), `retro` (look back over this session or recent logs for environment improvements), `domain-modeling` (terms and ADRs), `laravel-herd-worktrees` (worktree plus `.test` URL).

## Running out of context

Order matters: the cheapest move that preserves the primary source wins:

1. **Keep going** while the work still fits. Most sessions never need any of the rest.
2. **Start a fresh session** when the next task is genuinely independent. Nothing to carry, nothing to lose.
3. **`handoff`** when the next agent needs what this session learned. It writes the document; you start clean with a primary source on disk.
4. **Delegate to a subagent** when the expensive part is legwork whose *conclusion* is all you need back.
5. **Compact last.** Summarising a grilling or diagnosis session replaces a primary source with a confidently-wrong paraphrase. Prefer `handoff`, which writes the record down before the context goes.

## When nothing fits

Say so plainly and answer the question directly. Reaching for the nearest skill because one must be named is worse than none: it spends a whole workflow on the wrong shape of problem.

Two skills exist for the meta-work rather than the work: `writing-for-agents` (writing any document an agent consumes) and `teach` (learn a concept inside this workspace). `wait-what` is the one to reach for when *this* answer did not land.
