---
name: fast-implement
description: "Implement a piece of work in a single session, without the coordinator pipeline's approval gates."
disable-model-invocation: true
---

# Fast implement

**Objective:** Implement the work described by the user in the spec or tickets, in this session, with
no architect step, no independent QA role, and no coordinator approval gates.

This is the short path. Use it for a ticket whose direction is not in question and whose blast radius
is small. For anything else use `/implement`, which runs the gated architect → developer →
code-review → QA pipeline.

## Execution in Three Phases

A strict pipeline, resolved in order: **Pre-flight** (confirm the ticket is actually startable, and by this agent) → **Coding** (TDD, tests, an explicitly approved review, commit, and push) → **PR & Wrap-up** (offer the separate `/to-pull-requests` command). Only the developer can select `/to-pull-requests`.

### Phase 1: Pre-flight

1. **Resolve the ticket.**
    - **A specific ticket is named** (an issue number, URL, or a `.scratch/<feature>/issues/NN-*.md` path): use it.
        - **Fail fast on `hitl`:** if it carries `hitl` (see `docs/agents/triage-labels.md`), stop immediately and tell the user to run `/to-guide` instead — don't check anything else on this ticket, this agent only implements `afk` work.
        - **Fail fast without `pipeline::fast`:** for an `afk` ticket, require the explicit `pipeline::fast` label (GitHub/GitLab) or `**Pipeline:** pipeline::fast` field (local tracker) — see `docs/agents/triage-labels.md`. If the label/field is absent entirely or is `pipeline::full`, stop immediately and tell the user to run `/implement` instead.
    - **An epic is named** (carries `status::specs`, or is otherwise the parent of a decomposition) rather than a specific ticket: pick the next ticket yourself instead of asking. Never auto-pick a `hitl` ticket — that execution mode always routes through `/to-guide`, not this agent.
        - **GitHub/GitLab:** run the same frontier query `/wayfinder` uses (`docs/agents/issue-tracker.md#wayfinding-operations`), scoped to the epic's sub-issues and filtered to `pipeline::fast` + `afk` — open, unblocked, unclaimed, first in decomposition order. Claim the chosen ticket (`gh issue edit <n> --add-assignee @me` on GitHub, `glab issue update <n> --assignee @me` on GitLab) before any other write, the same way `/wayfinder` claims a ticket, so a concurrent session (e.g. a parallel worktree) doesn't pick the same one. If the filtered frontier is empty, stop and tell the user why: if open, unblocked, unclaimed tickets remain but all are `hitl`, say so and point at `/to-guide`; if unblocked `afk` tickets remain but none carry `pipeline::fast` (label missing or `pipeline::full`), say so and point at `/implement`; otherwise explain that nothing is unblocked yet, or everything is already claimed.
        - **Local tracker:** read each `.scratch/<feature>/issues/NN-*.md` file in filename order — a purely linear chain — and take the first one that is `**Workflow:** status::ready`, `**Execution:** afk`, and `**Pipeline:** pipeline::fast`. If tickets remain but every `status::ready` one is `hitl`, say so — naming them — and point at `/to-guide` instead of picking one; if `afk` ones remain but none carry `**Pipeline:** pipeline::fast`, say so — naming them — and point at `/implement` instead.
        - Once chosen this way, treat the ticket exactly like one named explicitly for the rest of this process.
    - **Nothing is named:** when this repo defines a git workflow doc (e.g. `docs/agents/git-workflow.md`) with an "Issue First" rule, stop and ask the user to name an existing ticket or run `/to-spec`/`/to-tickets` first — don't start the work. Otherwise, skip this check entirely.
2. **Check blockers**, on the resolved ticket, whatever its current `status::*` label. Read its blockers from this repo's tracker (native GitHub/GitLab dependency links, or the `Blocked by:`/`**Blocked by:**` field — see `docs/agents/issue-tracker.md`).
    - Any blocker still open → stop and tell the user which ones. Don't start the work. If the ticket isn't already `status::blocked`, set it (same label swap as step 3).
    - All blockers closed/resolved (or none) → continue. A `status::blocked` ticket passes through `status::ready` in step 3.
3. **Mark it in progress — mandatory, before creating the issue branch or editing any file.** This is not deferred to "later" and is not optional in a cloud or single-session run. A ticket carries exactly one `status::*` label (see `docs/agents/triage-labels.md`), so replace, don't add:
    - **GitHub:** `gh issue edit <n> --remove-label status::ready --remove-label status::blocked --add-label status::in-progress`, then confirm with `gh issue view <n> --json labels --jq '[.labels[].name]'` that `status::in-progress` is the only `status::*` label.
    - **GitLab:** `glab issue update <n> --unlabel status::ready,status::blocked --label status::in-progress`, and confirm the same way.
    - **Local tracker:** set the file's `**Workflow:**` line to `status::in-progress`.
    - If the label write fails, stop and report it; don't start coding on an unmarked ticket.
4. **Git pre-flight, before editing files:**
    - Resolve the exact integration branch from the ticket's `## Integration Branch` section or,
      for a child ticket that omits it, from its parent epic. An absent value is a blocker; do not
      infer a branch from memory, the current checkout, or a service name.
    - The current branch must match `branch_pattern` and be an issue branch. If it does not,
      fetch the integration branch and create `feature/issue-<ID>-<slug>` from it before coding.
      Never commit or push directly to the project base branch or an `integration/*` branch.

### Phase 2: Coding

1. Use `/tdd` where possible, at pre-agreed seams.
2. Run typechecking regularly, single test files regularly, and the full test suite once at the end.
3. Ask the developer: “Провести code review?” Stop for their answer.
    - **Yes:** run `/code-review`. It launches the Standards and Spec subagents through the coding application's manually configured mechanism, waits for both reports, and returns its separate `## Standards` and `## Spec` report to this primary session. Address any requested changes, then repeat the relevant tests before continuing.
    - **No:** record that the developer declined review and continue.
4. Ask the developer for explicit permission to commit and push. Stop for their answer.
5. After approval, verify that the current branch still matches `branch_pattern` and is neither `base_branch` nor `integration/*`; commit the completed work with a Semantic Commit Message and push it to the current issue branch. Report the commit and push result to the developer.

### Phase 3: PR & Wrap-up

After a successful push, offer `/to-pull-requests <ticket>` as the next command. Do not invoke it automatically, open a PR, run `qa-gate`, or close the ticket in this skill. Leave `status::in-progress` on the ticket: this skill never removes it. Closing the ticket and moving its unblocked dependents to `status::ready` belong to `/to-pull-requests` after the merge.