---
name: build
description: Take a scoped request or chosen design direction (Paper (paper.design), HTML, or Figma) to a verified candidate ready for the owner's local review — a gated implement-and-verify loop that runs pre-build-review before coding and post-build-review after, and never ships on its own. Use after your bootstrap workflow, after choosing a direction from prototype or paper-prototype, when continuing implementation, or when asked to build, implement, revise, or get a change ready for local review. Small UI papercuts take the shorter polish-fix path instead.
---

# Build a local candidate

Your bootstrap workflow opens the lane. `build` owns the implementation and
verification loop. Your ship workflow begins only after the owner reviews the
running result and says go.

## Assumes

Two stages you supply: a **bootstrap step** that creates the dedicated
worktree or checkout this skill requires, and a **ship step** that re-runs
`scripts/tree-fingerprint`, compares against `.build-review.scratch.md`, and
refuses to open a PR on a mismatch.

Do not create a worktree, commit, push, open a PR, approve the interface on
the owner's behalf, or invoke `grill-with-docs` automatically.

## Process

### 1. Confirm the lane

Run from a working copy dedicated to this change — a worktree or separate
checkout — never the primary checkout. If you are in the primary checkout,
stop and run your bootstrap workflow first.

Read the project's agent and contributor instructions (root and nested)
before planning. Recover the intended result from the request, issue, chosen
prototype, Figma direction, prior review, and nearby code before asking the
owner.

For UI work, confirm that a before-state screenshot exists before the first
edit. If it is missing, capture the untouched worktree or a matching
`main`/production surface. Never switch the feature worktree to `main` to
recreate it.

### 2. Clarify lightly

State a compact build frame only when it adds information:

- **Outcome:** what should become true for the user.
- **Already decided:** decisions this build must preserve.
- **Assumptions:** safe defaults the build will carry.
- **Major uncertainty:** at most three points that could materially change the
  result, each with a recommended answer.

Continue when an assumption is safe and reversible. State it inline instead of
asking for permission.

Ask one sharp question and pause when a wrong answer would cause substantial
rework, change the product model, affect ownership/permissions/lifecycle, create
materially different user experiences, or commit to a hard-to-reverse direction.

Recommend a manual `grill-with-docs` session when the uncertainty contains
conflicting domain language, an unresolved product boundary, or several
dependent product decisions. Never invoke it automatically. Route unresolved
interface direction to `paper-prototype` or `prototype`, then resume `build`
after the owner chooses.

### 3. Gate the plan

Run `pre-build-review` once the direction is settled.

| Verdict | Action |
| --- | --- |
| `Go` | Continue to implementation. |
| `Go with changes` | Incorporate the required plan changes, then continue. |
| `No-go` | Stop and return to the stage named by the review. |

Do not implement around an unresolved blocker. An explicit owner instruction
to proceed past a `No-go` counts as `Go with changes` — record the override
and its scope in the evidence file.

### 4. Implement

For user-facing frontend work, apply the `ui-craft` suite (`suites/ui-craft`
in this repo) when installed; otherwise follow the nearest existing patterns.
Build the smallest coherent change that satisfies the settled intent.

The owner runs the project's dev services; use the running preview and never
launch a competing instance. If no preview is running, ask the owner to start
it, and record any browser checks that could not run as `not run`. Verify
incrementally in proportion to the change, but leave the final gate to
`post-build-review`.

### 5. Review and repair

Run `post-build-review` automatically after implementation.

- Fix objective implementation, state, accessibility, responsive, or failed
  check findings, then run the review again.
- Return product, scope, or interface uncertainty to the stage named by the
  review: `grill-with-docs` for domain questions, `paper-prototype` or
  `prototype` for design direction, `pre-build-review` for plan-level state
  or scope gaps.
- Preserve subjective craft notes for the owner rather than silently
  redesigning.
- Stop and escalate risky auth, permissions, API, routing, or data surfaces
  the review cannot safely approve.

Any edit after a passing review invalidates that review. Repeat this step
before handoff.

### 6. Record the reviewed state

After `Pass` or `Pass with notes`, run this skill's
`scripts/tree-fingerprint` and write `<worktree>/.build-review.scratch.md`
(keep it out of version control — add it to `.git/info/exclude` if the
project does not already ignore scratch files). Ignoring the evidence file is
a correctness requirement for any other fingerprint tooling; this skill's
script skips it by name. Record:

- `head` from `git rev-parse HEAD`.
- `tree-fingerprint` from the script.
- `Pre-build verdict` — what step 3's gate returned, so the ship step can see
  the gate ran rather than assuming it.
- Verdict and review time.
- Checks run and their results, and every check the review recorded as `not run`.
- Preview URL and states exercised.
- Before/after evidence.
- Known non-blocking notes.

The fingerprint makes the review tamper-evident: your ship workflow re-runs
the script and compares, so any edit after the recorded review shows up as a
mismatch and sends the tree back to step 5. The file is handoff evidence, not
durable project documentation. Overwrite it after each passing review.

### 7. Hand off

Report:

- the exact preview URL and state the owner should inspect
- what changed
- the post-build verdict and evidence
- remaining notes or intentional differences from the chosen direction

End with `Ready for local review`, never `Ready to ship`.

The owner's feedback re-enters `build`; any resulting edit requires another
post-build review. Their go hands the unchanged tree to your ship workflow.
