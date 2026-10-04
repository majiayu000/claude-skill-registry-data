---
name: sk-flow
argument-hint: '[auto|manual]'
description: End-to-end slashkit workflow. Runs sk-explore, sk-alternatives, sk-planning, sk-implement, sk-review-and-fix (or sk-review), sk-verify, then sk-pr. Use when the user asks for /sk-flow, the full workflow, or "run the ai workflow".
---

# Flow

End-to-end flow: **Explore → Alternatives → Planning → Implementation → Review → Verify → PR**.

Only run this skill when the user explicitly asks for the workflow.

## Modes

- **manual** (default): ask before each phase.
- **auto**: run phases sequentially; still ask for missing critical input like the slug.

## Slug and flow folder

1. If the user provided a slug, use `.agents/flows/sk-<slug>/`.
2. If no slug, look for a stuck flow: any `.agents/flows/sk-*/` where the runbook has pending work. If one, suggest continuing its next pending phase or active PR. If several, list them and ask. If none, ask for a short kebab-case slug.
3. Create `.agents/flows/sk-<slug>/` if needed.
4. Start as a single-PR flow. Create or update `RUNBOOK.md` from `templates/RUNBOOK.md` and pass the slug to each phase.
5. If planning decides that the work needs multiple PRs, convert the root runbook to `templates/MULTI-PR-RUNBOOK.md` and follow the multi-PR contract below.

## Single-PR contract

Keep the current flat flow unchanged:

```text
.agents/flows/sk-<slug>/
├── RUNBOOK.md
├── 0 - EXPLORE.md
├── 1 - ALTERNATIVES.md
├── 2 - PLANNING.md
├── 3 - IMPLEMENTATION.md
├── 4 - REVIEW.md
├── 5 - VERIFY.md
└── 6 - PR.md
```

The runbook template is `templates/RUNBOOK.md`. State values are `done`, `skipped` (with reason), `diverged` (with reason), `blocked`, `in-progress`, and `pending`.

## Multi-PR contract

Planning owns the transition from a single-PR flow to a multi-PR initiative:

```text
.agents/flows/sk-<slug>/
├── RUNBOOK.md                 # initiative state and PR order
├── 0 - EXPLORE.md
├── 1 - ALTERNATIVES.md
├── 2 - PLANNING.md            # masterplan
├── pr-<stable-slug>/
│   ├── RUNBOOK.md
│   ├── 2 - PLANNING.md        # self-contained plan for this PR
│   ├── 3 - IMPLEMENTATION.md
│   ├── 4 - REVIEW.md
│   ├── 5 - VERIFY.md
│   └── 6 - PR.md
└── pr-<stable-slug>/...
```

- Use `templates/MULTI-PR-RUNBOOK.md` for the root and the normal `templates/RUNBOOK.md` inside every PR directory. Mark rows `0` and `1` in a PR runbook `skipped` because those artifacts remain at the initiative root.
- Derive each stable slug from the PR's purpose, not its ordinal number. Once recorded, never rename or reuse it even if PR order changes.
- Keep `Active PR` equal to exactly one PR slug, or `none` when the initiative is complete or blocked. Downstream phases use this field and the matching `Directory`; they never choose a plan from a glob or modification time.
- The root PR table is the source of truth for order, repository, dependencies, state, directory, link, branch, base SHA, and HEAD. Dependencies contain PR slugs or `none`.
- A PR is unblocked only when every dependency is `done`. Run one active PR through planning to PR before starting another.
- Before each phase, fetch refs and verify the checked-out branch and HEAD against the active PR row. Sync using the harness's supported workflow, then record the resulting HEAD in both runbooks. If safe sync is unavailable or the values disagree unexpectedly, mark the PR `blocked`; do not continue on guessed state.
- After `sk-pr`, record the PR URL, branch, base SHA, and final HEAD; set that PR to `done`. Then select the first `pending` PR in table order whose dependencies are all `done`. Set it to `in-progress` and update `Active PR`. If none is unblocked, set `Active PR: none` and mark the initiative `completed` or `blocked` as appropriate.

## Dispatch metadata

Dispatch each phase to a fresh isolated worker. When the harness has a subagent/task mechanism this is mandatory, not optional. In the runbook for the phase being executed, record its agent or session ID, parent dispatch ID or input artifact, and resulting HEAD when the phase can change the repository. Only when no isolated worker mechanism exists, record `inline` and explain the fallback in `Divergence / Notes`.

For multi-PR work, initiative coordination stays in the parent context. Phase dispatch metadata belongs in the active PR's runbook; the root table carries only cross-PR state.

## Delegating the flow or a phase

Delegate by reference, never by paraphrase. A worker prompt names the skill to invoke and carries only its inputs:

- Whole flow: the goal, the slug, the mode, and "invoke the `sk-flow` skill and follow it verbatim".
- One phase: the skill name (e.g. `sk-planning`), the slug, and the artifacts it consumes.

Never reduce a phase to "write `<N> - <NAME>.md`" or a checklist of artifacts. Artifacts are outputs, not instructions — a paraphrase silently drops every requirement that lives inside the skill (mandatory reviews, per-phase dispatch, runbook updates).

## Running one PR

1. **Explore** — `sk-explore`. Writes root `0 - EXPLORE.md`; updates row `0`.
2. (manual) Ask to continue.
3. **Alternatives** — `sk-alternatives`, including its mandatory `sk-review-alternatives` pass. Writes root `1 - ALTERNATIVES.md`; updates rows `1` and `1r`.
4. (manual) Ask to continue.
5. **Plan** — `sk-planning`, including its mandatory `sk-review-plan` loop. For one PR, writes root `2 - PLANNING.md`. For multiple PRs, writes the root masterplan and each PR directory's `2 - PLANNING.md`, initializes all runbooks, and selects the first unblocked PR.
6. (manual) Ask to continue.
7. **Implement** — `sk-implement`. Writes `3 - IMPLEMENTATION.md` in the active flow or PR directory; updates row `3` there.
8. (manual) Ask to continue.
9. **Review** — `sk-review-and-fix` by default, or `sk-review` if read-only. Writes `4 - REVIEW.md` beside the active plan; updates row `4` there.
10. (manual) Ask to continue.
11. **Verify** — `sk-verify` is required unless the agent is blocked (e.g. verification needs credentials, services, or an environment it cannot reach). Writes `5 - VERIFY.md` beside the active plan and updates row `5`; when blocked, mark row `5` `skipped` with the blocking reason and continue.
12. (manual) Ask to continue.
13. **PR** — `sk-pr`. Writes `6 - PR.md` beside the active plan; updates row `6`. Complete the single-PR flow, or update the initiative root and advance to the next unblocked PR.

## Example prompts

- `/sk-flow add-auth-token`
- `/sk-flow auto add-auth-token`
- `/sk-flow manual add-auth-token`
- `Run the full ai workflow for add-auth-token`
