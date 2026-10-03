---
name: big-project-manager
description: Run large projects via living spec and verified sub-agents.
version: 0.1.0
author: Darkgoatie
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [project-management, planning, delegation, spec, sub-agents, verification]
    related_skills: []
---

# Big Project Manager

For work too big to hold in one context, including taking over an existing repo's remaining work. Runs on a living spec: every step reads it, every change updates it. Skeletons for every spec file are in `templates/`.

## When to Use
Use for multi-session projects or finishing a repo: living spec, modules, verified sub-agents.

- A project or feature set too large for one context window.
- "Finish the rest of this repo" or taking over half-done work.
- Work that will span several sessions or several sub-agents.

Don't use for: single-file fixes, one-sitting features, or exploratory spikes on their own (run the spike, then come back here if it grows).

## 0. Inventory what exists
Before writing anything, list the repo's existing design docs (ARCHITECTURE.md, blueprints/, API maps, TODO.md, progress logs). Link to them from the spec; write only what is missing. Duplicating an existing doc creates two sources that drift.

If `docs/spec/` already exists, you are resuming: read HANDOFF.md and TASKS.md, then for every task marked in progress compare its listed commits with `git log --oneline`. Finish it, redo it, or mark it needs-fix before starting anything new.

## 1. Write the spec
In `docs/spec/` (or `plans/<project>/` when there is no repo):
- `SPEC.md`: goal, non-goals, constraints (platform, stack, performance), glossary, links to existing docs.
- `ARCHITECTURE.md` only if the repo has none: components, data flow, storage, key decisions with a one-line reason each.
- Open questions. Ask the user about anything that changes the architecture; decide low-stakes items yourself and note them.
- State the core model in one sentence and get the user to confirm it before anything else (e.g. "each tenant gets an isolated database behind one shared API"). A wrong core model silently shapes every later step.
- Risky unknowns (an untested library, a platform quirk, a performance ceiling): list them and plan a throwaway spike for each. Record the yes/no result and numbers in SPEC.md; delete the spike code.
Do not start implementing until the user has seen the spec.

## 2. Decompose into modules
For each module, `docs/spec/modules/<name>.md` with:
- Responsibility (one paragraph) and what it does NOT do.
- Public interface: functions/types/messages with signatures, inputs, outputs, errors.
- Invariants the implementation must hold, not just signatures. Examples: "non-blocking socket reads and writes buffer partial frames"; "no side vectors kept aligned by index with another list"; "an idle queue consumes no CPU".
- Dependencies: only other modules' interfaces, never their internals.
- Files it owns, and how to test it in isolation.
If two modules need each other's internals, the boundary is wrong. Fix the spec, not the code.

## 3. Baseline and smoke test
Before the first task:
- Record in SPEC.md: test pass/fail counts, build time, ERROR lines in a standard run, and the key performance numbers. Every review compares against these; any regression becomes a needs-fix task.
- Commit one smoke script (`scripts/smoke.sh` / `.ps1`) that builds, runs the tests, and runs a short real scenario with error counting. Every task must pass it, so "verified" means the same thing for every agent.

## 4. Tasks in TASKS.md
- `docs/spec/TASKS.md`, committed: small tasks (one sitting, a few commits), each with module, files touched, dependencies, and an observable acceptance check. "Tests pass" is not enough: name something you can see or measure ("a 60 s run of the standard scenario has 0 ERROR lines", "a client that stops reading for 2 s stays connected").
- Number tasks and never renumber; users and reports refer to "task 14". Ideas raised mid-run are appended as pending with a new number and do not interrupt the current task.
- Order: first a thin end-to-end slice (the real entry point exercising the core model with minimal features), then widen. It exposes a wrong architecture while it is cheap to change.
- Size by cost too: long runs re-send a growing context every call, so cache reads dominate spend. Give each task a context budget, pin a reasoning effort (lower effort is several times cheaper for routine coding), and log each task's cost in TASKS.md so oversized tasks show. Treat budgets as defaults; tune them to the model and pricing in use.
- Support a `STOP` marker line: the runner halts there and waits for the user.
- Review the list before executing: merge trivial steps, split vague ones, reorder by dependency, drop anything outside the spec. Show it to the user and adjust.
- Status per task: pending / in progress / done / needs-fix / reverted, with commit hashes and attempt count.

## 5. Delegate with focused context
Applies to any sub-agent mechanism (built-in subagents, spawned CLI agents, a second session). Without one, run tasks sequentially yourself under the same rules.
- Pass only: the task text, that module's spec file, the interfaces of modules it calls, the exact files it may touch (as paths), the acceptance check and verification commands. Do not paste SPEC.md, other modules' specs, or unrelated source.
- Tell it to read only the listed files plus what they directly import, not to explore the repo, and to report back if it needs anything else instead of searching for it. Children given freedom to look around spend most of their context reading.
- Tell it not to edit other files, to report needed interface changes instead of making them, to commit each piece separately, and never to reset/rebase/amend/stash.
- Never put secrets, tokens, or `.env` contents in a child's context; give it the variable name and let the environment supply the value.
- Each child appends short progress lines to `docs/spec/progress/<task-id>.log` (step started, command run, result) so status is readable without the transcript.
- Protect the user's uncommitted work with a pre-commit hook that rejects commits touching files outside the task's list, not just a prompt rule.
- Parallel only when file sets are disjoint and each child has its own git worktree; otherwise they share the index and collide. Default to sequential.
- A one-shot child reads its prompt at start. Edit a task file before its turn, never while the runner may be starting it; if you must, stop and relaunch it.

## 6. Review every task (the child's report is not proof)
- Re-run the smoke script on a clean worktree of the commit and compare with the baseline.
- Count ERROR lines in every runtime log, not just panics.
- Search the test diff (`git diff <base>..<head> -- <test paths>`) for new early returns, skip markers (`#[ignore]`, `@pytest.mark.skip`, `it.skip`), or removed asserts: children weaken flaky tests instead of fixing them.
- Search the codebase for callers of each new public function; tested-but-never-called code is a common gap.
- Run a real end-to-end scenario for the feature (the actual binaries, the actual user action), including the reverse path (pause then unpause, disconnect then reconnect).
- Changed data formats, schemas, save files or config: require a migration and a test that loads data written by the previous version.
- New dependencies: check license and size, and record a one-line reason in the module spec.
- Reject and split any task that landed as one giant commit.
- Check `git reflog` for resets and `git status` for the user's files: both unchanged.
- Findings become new tasks in TASKS.md (needs-fix), fixed before dependent work.

## 7. Stop, escalate, roll back
- Two failed attempts at the same task: stop. Split it or ask the user; do not send a third identical attempt.
- A child reports it needs an interface change: pause the run, update the module spec, get approval for anything architectural, then continue.
- A landed task that fails review: `git revert` its commits (never reset), mark it reverted, and move tasks that depend on it back to pending.

## 8. Update the spec after every change
After each task lands: update the module file (interface, invariants, files), ARCHITECTURE.md if a decision changed, TASKS.md status and cost, and HANDOFF.md (current state, what is blocked, next task). Record deviations in one line. Commit with the code or right after. Never leave code and spec disagreeing.

## 9. Report
After each task: commits, what you verified yourself (numbers vs baseline), cost, what is still open. Keep it short; don't replay the process.

## 10. Definition of done
The project is done when: every task is done or explicitly dropped by the user, the spec matches the code, the smoke script and a full end-to-end run pass with no regression against the baseline, HANDOFF.md reflects the final state, and a final report lists total cost and known limitations.

## Pitfalls
- Skipping the spec for "quick" pieces: that's where boundaries rot.
- Giant tasks ("implement backend"): split until each has one acceptance check.
- Feeding a sub-agent everything, or letting it browse: it wanders, edits unrelated files, and costs tokens.
- Updating the spec in batches at the end: it goes stale mid-project.
- Trusting "no panics": a run with zero crashes can still log thousands of handled errors.
- Resuming from memory instead of from TASKS.md and git log: half-finished tasks get marked done.
- Retrying a failing task unchanged: the third attempt fails the same way.

## Verification
- [ ] SPEC.md states a core model the user confirmed, with baseline numbers filled in.
- [ ] Every module listed in SPEC.md has a file under `modules/` with interface, invariants and owned files.
- [ ] TASKS.md: every task has an acceptance check, a status, and commit hashes if done.
- [ ] Every done task was reviewed by you (smoke script, error counts, end-to-end run), not only by its child.
- [ ] HANDOFF.md matches the current `git log`.
- [ ] No code change is left without a matching spec update.
