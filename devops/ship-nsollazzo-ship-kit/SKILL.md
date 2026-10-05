---
name: ship
description: |
  Take a finished change from working tree to a green, mergeable PR by chaining
  simplify → verify → code-review → smart-commit → branch hygiene → PR → babysit →
  reflect. Use when the user says "ship", "ship it", "ship this", or wants the full
  clean→verify→review→commit→PR→green pipeline in one command. Default stops at approved
  + CI green + mergeable; does NOT merge unless --merge.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "[--fast] [--merge] [--no-monitor] [--no-verify] [--yolo]"
---

# Ship — working tree to green PR, one command

Orchestrate the kit's other skills in order. This skill only owns **sequencing, gates,
state, and the final report** — never re-implement a stage's logic inline.

## How to invoke each stage (portability)

Every stage names a skill **bundled in this kit** (`simplify`, `verify`, `code-review`,
`smart-commit`, `babysit`, `merge-and-monitor`, `reflect`). Run each by whatever mechanism your
agent provides:

- **If your harness has a skill-invocation tool** (e.g. Claude Code's `Skill` tool), call
  the named skill with it.
- **Otherwise**, load that skill's `SKILL.md` from this kit and follow its procedure
  directly — the bundled skills are written to be executed by reading them.

Either way: invoke the **exact skill named**, and don't substitute a similarly-named
subagent or generic tool for it.

**For `simplify`, `verify`, and `code-review` specifically: prefer your harness's native
or built-in skill of that name if it has one** (it's usually richer — e.g. a cloud
multi-agent reviewer), and fall back to this kit's bundled copy only where the harness
provides none. The bundled copies exist so the pipeline runs *everywhere*, not just where
those skills are pre-installed.

## Flags (parse from the arguments)

| Flag | Effect |
|------|--------|
| `--fast` | Skip Stage 1 (simplify) and Stage 3 (code-review) — for tiny changes |
| `--merge` | Squash-merge once green, then follow the deployment it triggers to a verified-healthy state (delegates to `merge-and-monitor`). Default: stop at green, human merges |
| `--no-monitor` | With `--merge`: merge and stop, skipping deployment monitoring. For repos with no CD, or when you only want the merge |
| `--no-verify` | Skip Stage 2b (runtime verify) — docs/config-only changes. The Stage 2a rebase check still runs |
| `--yolo` | Hands-off: auto-confirm the Stage 6 checkpoint and resolve any mid-pipeline ambiguity autonomously (operates under the bundled `yolo` skill's rules) instead of pausing. Stops at green — does **not** merge; merge stays `--merge` |

## Cross-cutting rules

- **Fail loud, never skip silently.** A stage that fails HALTS the pipeline with the
  evidence. A stage skipped by flag must be named as "skipped (--flag)" in the final
  summary. Never report "shipped" if anything was silently skipped.
- **Always simplify + review the full change being shipped.** Stages 1 (simplify) and 3
  (code-review) run on *every* ship — regardless of whether the work is already committed
  or a PR is already open. `--fast` is the **only** way to skip them. "The change being
  shipped" = uncommitted working-tree edits **plus** any already-committed-but-unmerged
  work (`git diff <base>...HEAD`), not just what's currently uncommitted — so your code
  gets simplified and reviewed even after you've committed or opened the PR. Any fixes
  they produce are committed (Stage 4) and pushed (Stage 7) like any other work.
- **Project conventions override this recipe.** A repo's own instruction file
  (`CLAUDE.md`, `AGENTS.md`, etc.) wins. Examples: a project that forbids a tracked
  CHANGELOG.md (skip smart-commit's changelog step there); a project whose tests run in a
  specific environment (CI, a container, a remote host) rather than locally; a
  project-specific verify/test recipe always beats the generic one.
- **State file** `.ship-state.json` (repo-local): write
  `{branch, head_sha, flags, completed_stages: []}` after each stage; on invocation, if it
  exists and `branch` matches the current branch, offer to resume from the next stage;
  delete it on success.

## Stage 0 — Preflight

1. Parse flags. Read state file → offer resume if it matches the current branch (under
   `--yolo`, resume automatically — don't ask).
2. `git status` + check for unshipped commits + `gh pr view --json url,state 2>/dev/null`.
   Detect unshipped commits robustly: `git log @{u}.. 2>/dev/null` works only when an upstream
   is set — a branch that has never been pushed has no `@{u}`, so that command errors and a bare
   `2>/dev/null` makes it look falsely "empty" (= nothing to ship). When there is no upstream,
   fall back to `git log <base>..HEAD --oneline` so brand-new local commits still count. If the
   tree is clean, there are no unshipped commits, AND no open PR exists for this branch → say
   "nothing to ship" and stop.
3. **PR already open for this branch:** an open PR does NOT skip the quality stages —
   "pushed" is not "polished", and a local review pass is cheaper than a remote review
   round-trip (push + CI + re-review). Adjust as follows:
   - **Run stages 1–4 against the PR's full diff vs base** (`git diff origin/<base>...HEAD`),
     not just the working tree — regardless of the PR's current approval state. If they
     produce fixes, commit (Stage 4) and continue; if they produce nothing, say so and
     continue.
   - **Even when the PR is already APPROVED + CI green + mergeable, still run them** (the
     always-simplify+review policy applies here too). ⚠️ Pushing the resulting fixes
     re-triggers CI and a fresh review, which can flip the existing approval — that's the
     accepted trade-off, not a surprise. Make it explicit in the Stage 6 checkpoint summary
     so the push is a deliberate choice; the Stage 6 gate (unless `--merge`) is the user's
     last chance to decline burning the green.
   - **Stage 5 is N/A**: never rename a branch with an open PR — deleting/repushing the
     remote ref closes the PR.
   - **Rebase (Stage 2a) becomes report-only**: report how far behind base the branch is,
     but don't rebase — once a PR is under review, babysit owns the decision of when an
     update-with-base is worth a re-review cycle.
   - **Stage 6/7**: the checkpoint gates pushing new fix commits to the existing PR
     (instead of "open PR?"); `--merge` authorizes it as usual. Stage 7 is just `git push`
     — no PR creation.
   - The final summary must still list every stage as run / produced-nothing / N-A with the
     reason — never silently omit them.
4. **Branch safety:** if on `main`/`master` with uncommitted work, create a working branch
   NOW (`git checkout -b wip/ship-<short-desc>`) before any stage mutates files. The final
   name is fixed in Stage 5 — don't bikeshed it here.
5. **Base branch:** resolve the branch this change targets. If a worktree/host tool records
   it (e.g. a `target_branch` field), read it from there; otherwise use the repo default
   (`git remote show origin` / `origin/HEAD`). Record it for Stage 7. (The fast-path needs
   this too — resolve it before the behind-base check.)

## Stage 1 — Simplify (skip if --fast)

Run the `simplify` skill on the **full change being shipped** (see *Always simplify +
review* — working-tree edits plus already-committed-but-unmerged work,
`git diff <base>...HEAD`, not just uncommitted). It applies quality cleanups to those
files; if the change was already fully committed, its edits land in the working tree and
are picked up by Stage 4.

## Stage 2 — Verify (skip if --no-verify)

**2a. Rebase check (runs even with --no-verify):** verification against a stale base is
worthless, so first check whether the branch should rebase onto the Stage 0 base branch:

```bash
git fetch origin <base>
git rev-list --count HEAD..origin/<base>            # commits we're behind
git diff --name-only HEAD...origin/<base>           # files base changed since we diverged
```

- Behind 0 commits → no rebase, continue.
- Behind, and base touched **any file this branch also touches** (compare against
  `git diff --name-only <merge-base> HEAD` + working-tree changes) → **rebase now**
  (`git stash` if dirty → `git rebase origin/<base>` → `git stash pop`). Overlap means the
  verify result would be a lie without it.
- Behind on disjoint files only → rebase anyway if it's cheap and clean (default), but a
  conflict here is not worth fighting pre-PR — abort the rebase and continue, noting
  "N commits behind base, disjoint, rebase deferred" in the Stage 6 summary.
- **Rebase conflict on overlapping files → STOP** (fail loud): abort the rebase, report
  the conflicting files, and ask the user how to resolve. Never auto-resolve conflicts in
  shipped code.

**2b. Verify:** run the `verify` skill: run the app/tests and observe the change actually
working (post-rebase, if one happened).
**Gate:** if verification fails → STOP. Report exactly what failed and why the pipeline
halted. Do not continue to review or commit broken work.

## Stage 3 — Code review (skip if --fast)

Run the `code-review` skill with `--fix`, reviewing the **full change being shipped** (the
diff vs base, per *Always simplify + review*) — so already-committed code is reviewed too,
not just uncommitted edits. There's no effort knob: `code-review` gets its thoroughness by
fanning out across parallel sub-agents (scaled to the diff), then adversarially verifying
each finding — so the depth is automatic.

`--fix` is essential here: it *applies* the findings to the working tree so Stage 3 can
re-verify and Stage 4 can commit them. A review that only reports (no fix) does not satisfy
this stage. (On Claude Code, prefer the built-in `code-review` skill, which has `--fix` and
a cloud `ultra` mode; elsewhere the bundled `code-review` covers it.) In particular, do
**not** dispatch a report-only review *agent* in place of this skill — e.g. on Claude Code
the `pr-review-toolkit:code-reviewer` / `silent-failure-hunter` agents *report* findings but
never apply them, so using one here leaves the findings unfixed and Stage 4 commits
un-reviewed-fixed code.

If it applied fixes AND Stage 2b (verify) ran: re-run the cheap verification (tests, not
the full app walk) so review fixes are never committed unverified. Same gate as Stage 2.
(Under `--no-verify`, Stage 2b was skipped, so there's nothing to re-run — the always-on
2a rebase check does not count as verification here.)

## Stage 4 — Commit

Run the `smart-commit` skill to cluster and commit with conventional messages.
Honor project conventions: where a tracked CHANGELOG is forbidden, tell smart-commit to
skip its changelog step. smart-commit's docs-drift step keeps README/docs in sync with the
change so any doc fixes land in the same PR.

## Stage 5 — Branch naming

The branch must match `<type>/<kebab-slug>` where `<type>` ∈ {feat, fix, docs, chore,
refactor, test, perf} — derive it from the dominant conventional-commit type of the commits
being shipped; slug = short kebab-case summary of the change.

- Non-conforming (wip/ placeholder, personal prefix, etc.) → `git branch -m <type>/<slug>`
  BEFORE pushing.
- Already pushed under the old name → push the new name, then after the PR is open delete
  the old remote ref (`git push origin :<old-name>`).
- Already conforming → leave it alone.

## Stage 6 — CHECKPOINT (the one pause)

Present a compact summary: stages run (and skipped, with flags), verification evidence,
review findings fixed, commit list, final branch name, drafted PR title + body.

Then **ask the user once, in plain text, to confirm: proceed to push + open PR?** Wait for
their reply. (If your harness has a structured multiple-choice prompt, you may use it; if
not, a plain "proceed? (yes/no)" in chat is the portable form. Either way — wait for an
answer; don't assume one.) This is the only outward-facing gate. Authorization rules:

- `--merge` on the invocation **is** standing authorization for all outward-facing steps
  (push, PR, merge, and the post-merge deployment watch) — do not re-ask at the checkpoint.
  The user opted into hands-off end-to-end by passing it. Monitoring is read-only observation:
  `merge-and-monitor` inherits babysit's "never mutate external state to force a gate green"
  rule.
- `--yolo` auto-confirms this checkpoint (hands-off through push + PR + babysit-to-green) —
  don't re-ask. It does **not** authorize merge: that stays `--merge`. So `--yolo` alone
  stops at green; `--yolo --merge` runs fully hands-off including the squash-merge. (The one
  thing `--yolo` does not silence is Stage 10 `reflect`, which never auto-writes — on a
  hands-off run it *surfaces* its suggestions without blocking; see Stage 10.)
- With a PR already open: the checkpoint gates pushing new fix commits to it (a push
  re-triggers CI + QA review). If the quality stages produced nothing, there's nothing to
  gate — record the checkpoint as N/A.
- Without `--merge` or `--yolo`, and with new work to push: the checkpoint question is
  mandatory. If running non-interactively (headless, or under an unattended loop), stop here
  and report "staged and waiting" rather than guessing.

## Stage 7 — Push + PR

1. `git push -u origin <branch>`.
2. `gh pr create` against the Stage 0 base branch. Body: what changed, why, how it was
   verified (cite the Stage 2 evidence). PR title must be conventional-format (some repos
   gate on it with a `pr-title` check). End the body with your standard attribution footer.

## Stage 8 — Babysit to green

**Invoke the `babysit` skill** (via your harness's skill tool if it has one; otherwise load
`babysit/SKILL.md` and follow it) to drive the PR to the goal (fresh APPROVED + all CI green
+ mergeable). The Stage 6 checkpoint already authorized hands-off continuation — don't ask
again.

babysit **owns its own loop** — it runs pass after pass until the goal. **Do not reimplement
it here, and do not substitute a hand-rolled `gh pr checks` poll** — that skips babysit's
React protocol (verify findings, reply on threads, resolve). Your only job this stage is to
invoke babysit and let it run to the goal, or report when it's genuinely blocked on a human
reviewer.

For a single status pass instead of the full loop, invoke `babysit` for one pass.

## Stage 9 — End state

- **Default:** report "PR #N is green and mergeable: <url>" and STOP. A human merges.
- **--merge:** invoke the `merge-and-monitor` skill in **from-ship mode** — pass `--from-ship`,
  the PR number, `--base <Stage 0 base branch>`, and `--squash`. Because Stage 8 (babysit) already proved
  the PR is fresh-APPROVED + CI-green + mergeable, merge-and-monitor **skips its own Step 1
  readiness gate** and starts at the merge. It then locates the deployment the merge triggers,
  watches it to completion, and verifies health.
  - Repo has no deployment pipeline → merge-and-monitor says so plainly and stops after the
    merge. Same end state as a bare `gh pr merge`; do not invent a monitoring step.
  - Deploy run fails → merge-and-monitor HALTS with the failing log. Report it as a halted
    stage. **Do not retry the deploy from here** — the merge already landed, so this is now an
    incident, not a pipeline stage.
  - `--no-monitor` → run `gh pr merge <PR#> --squash --delete-branch` inline and stop.
- Delete `.ship-state.json`.
- Final summary must list every stage as run / skipped (--flag) / halted — no silent gaps.

## Stage 10 — Reflect (final step)

Run the `reflect` skill as the very last action, after the end-state report — so every ship
ends by capturing what the session taught (gotchas, new patterns, integration quirks) into
the knowledge base. Under `--merge` this means reflect runs *after* merge-and-monitor's
report, so deploy-stage gotchas are in scope for capture too.

Reflect is safe to run on every ship: it **self-gates** (scans the session and early-exits
with "No new knowledge" when the work was routine) and **never auto-applies** — it proposes,
then waits for a plain reply (`ok`/`ko`) before writing anything. Under `--merge`, `--yolo`,
or any unattended/headless run there is no one to reply, so it only *surfaces* its suggestions
in the final report and does **not** block — it skips the save rather than waiting (it never
auto-writes, so nothing is lost but the optional capture). An interactive run still gets the
`ok`/`ko` prompt. Either way the pipeline completes — `reflect` never holds a hands-off run open.
