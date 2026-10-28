---
name: push
description: >-
  Use when the user asks to push the current branch — confirms a first-time
  upstream and a diverged main, and refuses force pushes without explicit
  authorization. Not for committing or reviewing. Self-contained — execute the
  inlined steps directly.
argument-hint: optional branch name (defaults to current branch)
---

<!-- GENERATED FROM framework/atoms/push.md via scripts/generate-skill-composites.ts — DO NOT EDIT BY HAND -->

# Task: Safe Git Push

## Overview

Push the current branch to its remote with a strict safety contract that reflects flowai's solo-maintainer-but-shared-repo norms. The skill never silently rewrites remote history, never pushes to a protected branch when the remote has diverged, and never sets an upstream without the user's explicit confirmation that the branch should track.

## Context

<context>
`git push` is one of the few operations that has side effects outside the local working tree. This skill encodes the project's safety expectations: pre-flight checks, explicit user gates on irreversible actions, and post-push verification that local `HEAD` actually matches the remote tracking ref. Consumed standalone via `/flowai:push` and as the final phase of the `ship` composite.
</context>

## Rules & Constraints

<rules>
1. **No `--force`**: never run `git push --force` (or `git push -f`). If the user explicitly asks for force-push, decline and explain `--force-with-lease` as a safer alternative.
2. **`--force-with-lease` requires per-push confirmation**: even with the lease flag, ask the user once per push attempt — never inherit authorization from a previous push in the same session.
3. **First push gate**: if the branch has no upstream (`git rev-parse @{u}` fails), ASK the user "Should this branch track `origin/<branch>`? I would run `git push --set-upstream origin <branch>`." Wait for an affirmative reply before pushing.
4. **Protected-branch divergence gate (HARD REFUSAL)**: if the remote branch is `main` / `master` AND the remote has commits the local does not (`git rev-list HEAD..@{u}` is non-empty), REFUSE `--force` AND `--force-with-lease` absolutely — explicit per-push user authorization does NOT unlock force on a protected diverged branch (the canonical regression: destroying a teammate's commits). The only allowed paths are: (a) `git pull --rebase` (or merge) and then a normal fast-forward push; (b) abort. Do NOT present `--force-with-lease` as an option in the question; if the user volunteers "force", "overwrite", or "force-with-lease", restate the refusal and re-offer pull-rebase / abort.
5. **Target-branch sanity**: refuse to push a branch other than the current one (`git push origin <other>` from `<current>`) unless the user explicitly types the target branch name. The default is always the current branch.
6. **Post-push verification**: after a successful push, run `git rev-parse @{u}` and `git rev-parse HEAD`; they MUST be equal. If they differ, the push reported success but the upstream did not advance — surface the discrepancy and STOP.
7. **Git pager off**: use `GIT_PAGER=cat` for all git commands so output is non-interactive.
8. **No PR creation**: this skill ONLY pushes. PR creation (`gh pr create`, etc.) is out of scope and is left to the user or a separate skill.
9. **CI-await contract** (FR-ATOM-PUSH.CI-AWAIT): when AGENTS.md declares a `## CI/CD` section, the atom MUST wait for the CI run triggered by the pushed SHA to reach a terminal state (≤30 iterations × 60 s = 30 min cap), and on failure MUST hand off to the `investigate` skill with run URL + failed-job logs. The wait is NOT optional — no per-push opt-out. Malformed `## CI/CD` (missing `Provider` or `Status command`) → STOP fail-fast. Absent section → skip silently. Status command MUST be single-shot (exit 0 / 1 / 2 / other) — blocking-wait commands (`gh run watch --exit-status`, `glab ci status --wait`) defeat the iteration cap and are NOT acceptable.
</rules>

## Instructions

<step_by_step>

1. **Identify Target Branch**
   - Run `git rev-parse --abbrev-ref HEAD` to identify the current branch as `<CURRENT>`.
   - If the user typed a branch name as argument, compare to `<CURRENT>`. If different, STOP and ask "You typed `<typed>` but the current branch is `<CURRENT>`. Push `<CURRENT>` or check out `<typed>` first?". Wait for an answer.
   - Otherwise, the push target is `<CURRENT>`.

2. **Resolve Upstream**
   - Run `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null` to find the upstream of `<CURRENT>`.
   - If the command exits non-zero (no upstream), ASK the user: "`<CURRENT>` has no upstream. Should I run `git push --set-upstream origin <CURRENT>`?". Wait for an answer.
     - Affirmative → proceed to step 3 with `--set-upstream origin <CURRENT>`.
     - Negative → STOP. Report "No upstream and user declined to set one — nothing to do."

3. **Safety Checks**
   - **Protected-branch divergence (HARD REFUSAL — see Rule 4)**: if the upstream is `origin/main` or `origin/master`, run `git fetch origin <CURRENT>` then `git rev-list --left-right --count HEAD...@{u}`. If the right count (commits the remote has and local does not) is > 0, ASK the user with EXACTLY two options: "Remote `<CURRENT>` is ahead by N commit(s) the local branch does not have. Force is REFUSED on protected branches even with explicit authorization. Pull and rebase first, or abort?". `--force` / `--force-with-lease` are NOT options — never present them, never run them, even if the user volunteers "force", "overwrite", or "yes I want to overwrite the remote". If the user pushes back, restate the refusal and re-offer pull-rebase / abort.
   - **Non-protected branch divergence**: if the right count > 0, surface the divergence but proceed with a regular `git push` (which will fail safely if non-fast-forward). DO NOT proactively suggest force.
   - **`--force` request**: if the user has explicitly asked for `--force`, decline. Explain `--force-with-lease` and proceed only with per-push user authorization (see Rule 2).

4. **Push**
   - Run `GIT_PAGER=cat git push [--set-upstream origin <CURRENT>]`. Stream stdout + stderr to the user. Do NOT silence error output.
   - On a non-fast-forward error: do NOT retry with `--force` or `--force-with-lease`. Surface the failure and STOP.

5. **Post-Push Verification**
   - Run `git rev-parse @{u}` and `git rev-parse HEAD`. Compare.
   - Equal → push succeeded. Report the remote ref and the pushed SHA.
   - Different → push reported success but upstream did not advance. STOP with "Post-push verification FAILED: @{u} = `<remote>`, HEAD = `<local>`. Investigate before retrying."

6. **Await CI** (FR-ATOM-PUSH.CI-AWAIT)
   - Read AGENTS.md `## CI/CD` section.
     - **Absent**: output `No CI declared in AGENTS.md — skipping CI await.` and continue to step 7 (`7. **TOTAL STOP**
   - Final report: target branch, upstream, pushed SHA, post-push verification result, CI await result (`skipped`, `green`, or `not reached — stopped earlier`).`).
     - **Malformed** (missing either `Provider:` or `Status command:`): STOP with `## CI/CD section is malformed — required keys: Provider, Status command. Found: <list of present keys>.` Do NOT silently fall back. Do NOT continue to step 7.
     - **Well-formed**: continue.
   - **Resolve tunables** (optional keys in `## CI/CD`):
     - `Poll interval:` — seconds between status polls. Default `60`. Accept integer seconds; a value `<5` is treated as malformed and STOPs the atom.
     - `Wall-clock budget:` — soft cap on total await time. Default `1800` (30 min). Accept integer seconds.
     - Compute `ITER_CAP = max(1, ceil(<budget> / <poll interval>))`. The iteration count — NOT wall-clock — bounds the cap so it stays deterministic across IDE-harness latencies. With defaults, `ITER_CAP = 30`; a project that sets `Poll interval: 10` and `Wall-clock budget: 60` gets `ITER_CAP = 6`.
   - Export the pushed SHA into the environment: `export SHA=$(git rev-parse HEAD)`. All CI commands below inherit `$SHA` from the agent's shell.
   - **Detect run trigger** (≤60 s window; sized at ~2× the slowest realistic provider lag, observed ~30 s for GitLab pipelines registering after push): invoke the `Status command`. Treat:
     - exit 0 or 1 (terminal on first call) → proceed straight to the poll loop branch.
     - exit 2 (in-progress — a run exists) → proceed to the poll loop.
     - any other exit → sleep 5 s and retry. After 12 retries (60 s) with no run detected, STOP with `CI declared but no run was triggered by $SHA within 60 s — verify the workflow trigger configuration.` Do NOT continue to step 7.
   - **Poll loop** (max `ITER_CAP` iterations × `<poll interval>` s sleep ≈ `<wall-clock budget>` wall-clock):
     - Invoke the `Status command`.
     - exit 0 → CI green. Continue to step 7.
     - exit 1 → CI red (terminal failure). Go to **Investigate Handoff** below.
     - exit 2 → still running. Sleep `<poll interval>` s. Re-invoke. Increment iteration counter.
     - any other exit → treat as a malformed Status command, STOP with the raw exit code and stderr.
   - **Iteration cap (anomaly)**: if `ITER_CAP` iterations completed without a terminal status (exit 0 or 1), STOP with a loud single-line message: `CI ANOMALY: <ITER_CAP> iterations × <poll interval>s = <budget>s elapsed without a terminal verdict. Run URL: <result of Run URL command if defined, otherwise "not available">. Last status exit: 2 (in-progress). Treat as an incident (hanging job, queue starvation, runner outage) — do NOT continue silently.` Do NOT invoke `investigate` (no failed-job logs to feed it yet — the build is still running, not red). Do NOT continue to step 7. The user owns the next action: extend the budget by re-running the atom after raising `Wall-clock budget`, cancel the CI run, or investigate the runner.
   - **Investigate Handoff** (CI red):
     1. If the `Logs command` is defined in AGENTS.md, execute it. Capture stdout. Truncate to 12 KB (`investigate` can fetch more via the run URL if it needs to drill deeper).
     2. If the `Run URL command` is defined, execute it. Capture stdout as the run URL.
     3. Do NOT assume the working tree is clean: `@{u} == HEAD` (step 5) proves only that the commit reached the remote, and a push leaves uncommitted work in place. The investigation therefore runs in a temporary worktree of the pushed commit, which is clean by construction; the handoff prompt below says so. Do NOT stash, reset, restore or commit the developer's uncommitted files to make the tree clean.
     4. Invoke the `investigate` skill via the host IDE's skill-invocation primitive (Skill tool / `/flowai:investigate` slash command / inline expansion of its `SKILL.md`) with this prompt:
        `CI failed for commit $SHA on branch <CURRENT>. Run URL: <URL or "not available">. Failed-job logs (truncated to 12 KB):\n<LOGS or "not available">\nDiagnose the root cause in a temporary git worktree of $SHA (git worktree add <scratch dir> $SHA), not in the current working tree, and remove that worktree when done. Do not apply a fix; report findings.`
     5. After `investigate` returns its report, STOP. Do NOT continue to step 7 — the push succeeded but the build is broken; the user owns the remediation decision.

7. **7. **TOTAL STOP**
   - Final report: target branch, upstream, pushed SHA, post-push verification result, CI await result (`skipped`, `green`, or `not reached — stopped earlier`).**

</step_by_step>

## Verification

<verification>
- [ ] Push target equals the current branch unless the user explicitly typed a different branch name AND confirmed the divergence.
- [ ] Upstream resolved; if absent, user explicitly authorised `--set-upstream`.
- [ ] No `--force` flag used. `--force-with-lease` used only after explicit per-push user authorization.
- [ ] Protected-branch (main/master) divergence: user explicitly resolved (pull/rebase or abort) before any push attempt.
- [ ] Post-push verification: `git rev-parse @{u}` matches `HEAD`.
- [ ] Git output streamed to user verbatim (no silenced stderr).
- [ ] CI await: when AGENTS.md declares `## CI/CD`, atom polled the declared Status command at the configured `Poll interval` (default 60 s) until terminal state or the `ITER_CAP = ceil(<Wall-clock budget> / <poll interval>)` cap (default 30 iterations).
- [ ] CI anomaly: when the iteration cap was hit without a terminal verdict, atom STOPped with the loud `CI ANOMALY` single-line message (run URL + last-known status) and did NOT silently skip to TERMINATION.
- [ ] CI failure handoff: failing-run logs (truncated to 12 KB) + Run URL passed to the `investigate` skill via skill invocation, with the instruction to work in a temporary worktree of `$SHA`; the developer's uncommitted files were left untouched; atom STOPped after `investigate` returned.
- [ ] CI absent: when AGENTS.md has no `## CI/CD` section, atom skipped the wait silently with a one-line note.
- [ ] CI malformed: when `## CI/CD` is present but missing `Provider` or `Status command`, atom STOPped fail-fast and did NOT continue to TERMINATION.
</verification>
