---
name: bootstrap
description: Finish step 0 of a project created from slipway — scaffold the app with the D-005 default, add check and test scripts with one real test, fill AGENT.md, get verify/meta/status green, open the bootstrap PR (carrying the uncommitted D-001 record), then run the BOOTSTRAP §3 acceptance probes the agent can run and list the rest for the owner. Use right after `new-project`, when `pnpm status` says "Step 0 — Bootstrap", or when the user says "bootstrap", "set up the project", "finish step 0".
---

# Bootstrap

Step 0 of the slipway path (`SLIPWAY.md`), after `new-project` has created the repository. The
reference for every step is `BOOTSTRAP.md` §1 and §3; this skill carries them out. Output is a
merged-ready PR, not a chat summary.

## Before anything

1. Run `pnpm status`. If its **Next** line is not "Step 0 — Bootstrap", say what it says and stop.
2. Run `git status`. Expect `decisions.md` modified (D-001, written by `new-project`) and nothing
   else unexplained. Anything else uncommitted: ask before touching it.
3. `git remote -v` must point at this project's repository, and `gh auth status` must be logged in.
4. Create the branch: `git checkout -b chore/bootstrap`. Never commit to `main` — it is protected
   (D-001), and the harness asks before any push.

## 1 — Scaffold the app (BOOTSTRAP §1)

The framework is decision D-005. Use the template default unless `decisions.md` D-005 already
records something else — then scaffold that and adapt the steps below.

1. Scaffold without prompts and without starting a dev server:
   `pnpm create vite apps/web --template react-ts` — if it asks anything, answer so that it
   neither installs nor starts (newer versions accept `--no-interactive`).
2. In `apps/web/package.json`:
   - `check`: the typecheck, e.g. `tsc -b` (the scaffold's `build` runs it too; `check` must exist
     on its own);
   - `test`: `vitest run`, with `vitest` added as a dev dependency;
   - keep `lint` and `build` as scaffolded.
3. Add **one real test**: a small pure function the app actually uses (e.g. a formatter in
   `src/lib/`), called from the UI, with a test that fails when the function is wrong. Prove it:
   break the function, run the test, see red, restore it (L-04 — commit first so the restore is safe).
4. From the repo root: `pnpm install`, then `node ci/verify.mjs --plan` — it must list `apps/web`
   under `check` and `test`. Then `pnpm verify` and `pnpm meta`, both green. Commit the lockfile.

The Stop hook starts enforcing `verify:fast` the moment the app exists: a red turn cannot end.
That is the harness working; fix the cause, never the gate. An approval prompt on a config edit
means you reached for a gate — stop and explain why before the owner approves anything.

## 2 — Fill AGENT.md

`new-project` filled the product, and the repository unless it ran with `--no-github` and no `--repo`; if
the Issue repo row still reads `<owner/repo>`, ask for it first. Three rows are the owner's to answer, one
question at a time and in their product's terms: the GitHub project (or none); the timezone deadlines and appetite dates
are read in (CI runs in UTC, so `local` there is UTC); and whether the product has money or other
correctness-critical math (the domain invariants doc, or `none`). Every other row keeps its default unless
the repo says otherwise (paths, gates, the domain map from `apps/` and `packages/`) — never ask about
those. When done,
`grep -n "<" AGENT.md` shows no placeholders, and `pnpm status` no longer reports Step 0.

## 3 — Open the bootstrap PR

Commit on the branch: the app, the lockfile, `AGENT.md`, and the D-001 edit in `decisions.md`
(plus a CI workflow update if `new-project` left one uncommitted). Push (the harness asks) and open
the PR from the template: `## What` with `Lane: bounded`, `## Verification` with the pasted output of
`pnpm verify`, `pnpm meta` and `pnpm status`, and `## Links` with `none: bootstrap`. Wait for CI:
`meta`, `verify` and `pr-body` must all be green. Do not merge — the owner does, after §4.

## 4 — Acceptance probes (BOOTSTRAP §3)

Each probe proves a gate can refuse. Run the ones below, **revert every one**, and paste the output
of each into a `## Acceptance run` section of the PR body. A probe you could not run is reported
as not run, never as passed.

**You run** (locally, on a scratch branch or with a revert in the same step):

| # | Probe | Expect |
|---|---|---|
| 1 | `pnpm meta` on a fresh clone (`git clone` into a temp dir) | PC1 green |
| 5 | add `"test:e2e": "echo x"` to `apps/web/package.json` | W1 red |
| 6 | add `continue-on-error: true` to a step in `ci.yml` (the harness asks — say it is a probe) | FO1 red |
| 8 | a review in `docs/reviews/` whose `Version line:` is not in the PRD | R1 red |
| 9 | a lesson with `review-by` in the past | L1 red |
| 10 | the sample commands in `process/harness/README.md` § Test | each hook prints; non-matches print nothing |
| 12 | two milestone files with `status: active` | MS1 `wip/exceeded` |
| 13 | M1 `status: active` while FRAME is `status: draft` | K1 `status/draft` |

**You run on GitHub** (on this private repository; clean up each one):

| # | Probe | Expect | Clean up |
|---|---|---|---|
| 3 | a throwaway branch with a failing test, pushed, draft PR | `verify` red, merge blocked | close PR, delete branch |
| 4 | temporarily empty the bootstrap PR's `## Verification` | `pr-body` red | restore the body, re-run |
| 7 | `gh issue create` with free prose (the intake hook will remind you — that is the probe too) | `needs-shape` label | close the issue |

**The owner runs** — list these in the PR as open items with exactly what to do:

| # | Probe |
|---|---|
| 2 | `git push origin main` from a clean checkout is rejected (or, where `main` could not be protected, turns CI red) |
| 10b | `git stash pop` in a session asks before acting |
| 11 | `/log-followup` files its issue in this repository |
| 14 | a new Claude Code session opens with the `pnpm status` state (ask it "what's next?") |
| 15 | asking the agent to edit `biome.json` or a workflow shows an approval prompt; a failing test stops a turn from ending — you will likely have seen this one already during §1; say so if you did |

## Finish

Report: the PR link, CI state, the probes run with their result, the owner's remaining probes, and
anything not verified. Then stop. After the owner merges, the next step is `/kickoff`.
