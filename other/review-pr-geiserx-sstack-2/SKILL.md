---
name: review-pr
description: Review one or more pull requests as a single Workflow run (three lenses, one fixer, one adversarial verifier), comment the plan on each PR, push the fixes, then merge or close. Use when asked to review, fix up or merge a PR, or on "review-pr".
---

# review-pr

Every review answers the same four questions, so nobody has to ask them:

1. Is this the right problem?
2. Is there a better way to fix it?
3. Is the fix robust: does it hold on the inputs, errors and platforms it will really meet?
4. Can we use it ourselves: do our own consumers of this repo get the change, and does it work for them?

The run is one Workflow script, so this skill is your opt-in to call the Workflow tool. You (the orchestrator) scout, write the script, read its result and merge. Agents inside the script never merge, and never spawn agents of their own. Without a Workflow tool, run the same stages as parallel agents yourself, in the same order.

Pin a model on every `agent()` call: the tier your CLAUDE.md sets for the lenses and the fixer, the strongest tier it allows for the verifier. An unpinned agent inherits the session's model.

## Steps

### 1. Scout

For each PR, fetch the title, body, author, base, head SHA, CI checks by name, linked issues, the full diff, earlier review comments, and whether "allow edits by maintainers" is on. Find our own consumers of the repo: other repos, deployments, scripts or docs that install, import, pin or call it (search the code host, lockfiles, compose files). Read the repo's CLAUDE.md, AGENTS.md and CONTRIBUTING.md, and how its last merged reviews were commented, so yours match.

Done when you can name, per PR, the head SHA, every required check, the PR type (ours or a contributor's, below), and the consumer list. An empty consumer list is fine if you searched for it.

### 2. Run the workflow

Write and run one script. Pass the step 1 facts in `args`. Several PRs go through one `pipeline()`, one item per PR; give each PR its own scratch clone.

**Lenses**, three `agent()` calls in `parallel()`, each blind to the others, read-only, each in its own fresh clone or worktree:

- `problem`: is this the right problem, and is there a simpler or more general fix? Compare with how the repo already solves similar things and with the issue that asked for it. Judge each feature of the PR on its own: keep, change or cut. A feature nobody would use is cut, not polished.
- `robustness`: reproduce. Run the failing case on the base, then on the head. Hunt error paths, edge inputs, concurrency, performance at real sizes, the other platforms or substrates the code runs on, and the reverse path (a new state needs a way out; a rule that lives in two places changed in both).
- `use`: run the head the way each consumer from step 1 would, on real data where it exists, read-only. Report what it would surface, how much is noise, what breaks, and what the consumer must change to adopt it (version pin, command, config).

Lens schema, required fields: `verdict` (`fix` | `merge-as-is` | `close` | `redesign`), `better_way`, `our_use`, `findings[]`, each with `severity` (`critical` | `high` | `medium` | `low`), `file`, `line`, `claim`, `evidence` (the command and its output, or the code read), `fix`.

**Fixer**, one `agent()` after the lenses (a barrier is right here: it needs all three reports). It drops findings it cannot reproduce or that fall outside the PR's intent, merges duplicates by root cause, takes a better way from a lens when it fits inside the PR, and decides. Then, in this order:

1. Posts one PR comment: what we will change and why, what we cut or leave and why. Plain words, file:line links pinned to the head SHA.
2. Commits the fixes, each with a test that fails on the PR's original head, and pushes. A fix with nothing to execute (docs, config, a skill) carries the check that shows it fixed instead: a validator run, a rendered page, a link check.

On a public repo, it scans the comment text, each commit message and the diff for private data before posting or pushing, the same scan the verifier runs. Nothing private may reach a public write, even once.

Fixer schema, required: `decision` (`fix` | `merge-as-is` | `close`), `comment_url`, `commits[]` (SHA and one line each), `dropped[]` (finding and reason), `new_head_sha`, `merge_pr` (the PR number to merge, which differs from the original when we opened our own), `adoption` (how each consumer takes the change).

**Verifier**, one `agent()` on the new head, prompted to refute and to default to "not mergeable". It:

- reproduces every fixed finding on the old head and shows it gone on the new one;
- mutates each new guard one line at a time and confirms a test goes red, then restores it (a test that cannot fail is a blocker);
- waits for CI on `new_head_sha` and reads every required check by name (a waiter that sees "no pending runs" right after a push reads green before the jobs register; an empty or skipped job list is not green);
- scans the full diff and every commit message for secrets, tokens, private hostnames, internal paths and personal data, with a positive control that proves the scan can match;
- re-reads the fixer's comment against what actually changed.

It may push a small, clearly correct fix itself and re-verify. Verifier schema, required: `verdict` (`merge` | `fix-again` | `close`), `head_sha`, `mutations[]` (guard, mutation, went_red), `checks[]` (name, conclusion), `privacy_hits[]`, `subject`, `body`, `notes`.

On `fix-again`, run the fixer and verifier once more with the verifier's notes. Stop after three rounds and report what is left.

Done when the script returns a verifier verdict for every PR.

### 3. Merge or close

Read the verifier result yourself. Merge only when the user asked for merging in this session; otherwise stop at a merge-ready report. Then, per PR, as its own step:

- **Merge** only when every required check on the final head is `success` and `privacy_hits` is empty. Re-read the checks with `gh pr checks` just before merging, then merge in a separate command, pinned to the head: `gh pr merge <n> --squash --match-head-commit <sha> --subject "<title> (#<n>)" --body-file <file>`. Without an explicit body, `gh` builds the message from the commits and adds a `Co-authored-by` line for every author it squashes. Admin bypass can merge a red PR, so the check comes first. Read the merge commit message back.
- **Close** with a comment that says why and what would make it mergeable.
- When we merged our own PR in place of a contributor's, close theirs by hand with a link to the merge commit. `Closes #N` acts on issues, not on pull requests.
- Then update every consumer from step 1 that needs it, or note the follow-up (a pin bump, a new command in a lane) where its owner will see it.

Done when each PR is merged or closed, each merge message reads as written, and each consumer is updated or has its follow-up noted.

## Our PR vs a contributor's PR

- **Ours**: the fixer commits straight to the branch.
- **A contributor's**: comment before every push. Push to their branch only when "allow edits by maintainers" is on. When it is off, put our commits on a branch of our own on top of theirs and open it as our PR; say so in the comment on theirs. Their commits keep their authorship on the branch. A squash merge makes the merge commit ours, so name them in its body; when the repo merges with merge commits instead, their authorship survives as is. If the repo runs CI on self-hosted runners, read the diff for workflow, build-script and secret-reading changes before any job runs. Thank them once, in the merge or close comment.
- **A public repo with a private consumer**: findings about the private consumer stay in the workflow's return value. The PR, its comments and its commits carry invented examples only.

## When to close instead of fix

Close when the `problem` lens and the fixer agree on one of these:

- the problem is not real, or not ours to solve here;
- a better fix means rewriting most of the PR (say what it is, and open it as our own PR if we want it);
- it duplicates or conflicts with merged work or another open PR;
- it adds a feature nobody here will use.
