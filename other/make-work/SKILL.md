---
name: "make-work"
description: "Read `docs/VISION.yaml` (goals and boundaries), `docs/ARCHITECTURE.yaml`"
---

# make-work command

Apply this command workflow. Treat any text after its invocation as the command input.

# Command: Make Work

Read `docs/VISION.yaml` (goals and boundaries), `docs/ARCHITECTURE.yaml`
(design and components), `docs/road-map.yaml` (release schedule and use-case
status), `docs/constitutions/design.yaml` (format rules), and the
software-requirements and use-case READMEs where they exist.

Then establish where the work actually stands. **Treat the tracker and the
roadmap as claims to verify, not as ground truth** — a task that builds on
"done" work fails when that work was never merged.

```bash
gh issue list --repo <owner>/<repo> --state all
```

For every release or closed issue that later work depends on:

- Confirm a **merged pull request** closed it. Closed-as-completed with no
  merged PR is not done (`gh issue view <n> --json stateReason`, then check its
  linked PRs).
- Confirm the implementation exists in the source tree, not just in the spec.
  Grep for the types, functions, or files it promised; find the commit in
  `git log`.
- Watch for stubs. A function returning a placeholder with an
  "implemented in a later release" comment is not an implementation.
- If the project exposes a readiness check (`mage status`), trust it over
  issue labels.

Anything failing those checks is unbuilt regardless of tracker state — plan its
implementation before anything that depends on it.

Run the consistency check if one exists (`mage audit`, or `mage analyze` where
it is named that way) to surface orphaned SRDs, use cases without test suites,
broken references, and use cases missing from the roadmap.

Then summarize: the problem the project solves, its architecture, what is
built versus in progress, which release is current and which of its use cases
remain, and the repo size from `mage stats` where that target exists.

## Proposing the work

Prioritize by release. Finish the earliest incomplete release's use cases
first; a later use case may be previewed when it shares functionality with the
current one. Map every issue to a use case in `road-map.yaml` — release 99.0
when unscheduled. Add to existing epics where they fit, propose new epics where
they do not, and say what must be built first and why.

Each proposed issue carries:

- **Type** — documentation (markdown under `docs/`) or code.
- **Required Reading** — the files the agent must read first. Mandatory.
- **Files to Create/Modify** — explicit, with the output path for docs and the
  packages for code.
- **Requirements, Acceptance Criteria**, and Design Decisions where they matter.
- Documentation issues additionally name their **format rule** and required
  sections. Code issues state acceptance as tests or observable behaviour, not
  as SRD-style goals.

Size code tasks at 300-700 production lines across no more than 5 files —
finishable in one session, substantial enough to matter. Split larger features;
combine trivial ones. **No more than 10 tasks at a time.**

**Propose the breakdown and create nothing** until we have agreed on it.

Then create each issue with `/gh-issue-push` rather than `gh issue create`: it
traces every file and field the change touches before drafting, and issues
written without that step miss cross-references. Link sub-issues to their parent:

```bash
gh api repos/<owner>/<repo>/issues/<parent>/sub_issues \
  --method POST \
  --field sub_issue_id=$(gh api repos/<owner>/<repo>/issues/<sub-number> --jq '.id')
```

After you implement work:

- Commit your changes with a clear message
- Log token usage: `gh issue comment <id> --repo <owner>/<repo> --body "tokens: N"`
- Close completed issues: `gh issue close <id> --repo <owner>/<repo>`
- File any new issues via `/gh-issue-push`; note them for the user if not created in this session
