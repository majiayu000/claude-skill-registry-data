---
name: fix
description: |
  Take a reported problem all the way to a green, mergeable PR: triage the issue with parallel
  sub-agents → cut a branch → implement the fix at the root cause → hand off to `ship`, which
  reviews, commits, opens the PR, and babysits it to a green approval. Use when the user says
  "fix it", "fix this bug", "debug and fix", "investigate and fix", or wants the whole
  diagnose-then-ship loop in one command. Read the issue from the argument. Pass `--yolo` to
  run hands-off (no questions) to a green PR; merge still needs `--merge`.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "[--yolo] [--fast] [--merge] [--no-monitor] [--no-verify] <issue description or reference>"
---

# Fix — reported problem to green PR, one command

The inbound sibling of `ship`. Where `ship` takes a *finished* change to a green PR, `fix`
*creates* the change: it diagnoses the problem, implements the fix, then delegates the entire
clean→review→PR→green pipeline to `ship`. This skill owns only **sequencing, gates, state,
and the final report** — it never re-implements a stage (triage's diagnosis, ship's pipeline)
inline.

## How to invoke each stage (portability)

The stages name skills **bundled in this kit** (`triage`, `ship`). Run each by whatever
mechanism your agent provides:

- **If your harness has a skill-invocation tool** (e.g. Claude Code's `Skill` tool), call the
  named skill with it.
- **Otherwise**, load that skill's `SKILL.md` from this kit and follow its procedure directly
  — the bundled skills are written to be executed by reading them.

Invoke the **exact skill named** — don't substitute a similarly-named sub-agent or a generic
"go debug it" for `triage`, or hand-roll a commit/PR flow in place of `ship`.

## Flags (parse from the arguments)

| Flag | Effect |
|------|--------|
| `--yolo` | Hands-off: never ask the user a question. Triage runs autonomously, the fix is implemented without a confirm-which-fix pause, `ship`'s checkpoint auto-confirms, and a stale resume state is taken without prompting. Operates under the bundled `yolo` skill's rules. Runs to a green PR — `ship`'s final `reflect` step only *surfaces* knowledge suggestions and never blocks (see Stage 4). Stops at green — does **not** merge. |
| `--merge` | Passed through to `ship`: squash-merge once green, then follow the deployment it triggers to a verified-healthy state (default: stop at green, human merges). |
| `--no-monitor` | Passed through to `ship`. With `--merge`: merge and stop, skipping the deployment watch. |
| `--fast` / `--no-verify` | Passed through to `ship` (skip simplify+review / skip runtime verify). |

Everything that isn't a flag is the **issue**: an error message, a failing test, a PR/issue
reference, or a described misbehavior. That's what Stage 1 triages.

## Cross-cutting rules

- **Fail loud, never skip silently.** A stage that fails HALTS the pipeline with the evidence.
  The final summary names every stage as run / skipped (--flag) / halted — never report
  "fixed" if anything was silently skipped.
- **The Iron Law (inherited from triage): no fix without a verified root cause.** If Stage 1
  can't reach one, STOP and report what's still unknown — never branch-and-guess.
- **Project conventions override this recipe.** A repo's own instruction file (`CLAUDE.md`,
  `AGENTS.md`, …) wins — its test/verify recipe, its branch rules, its CHANGELOG policy.
- **State file** `.fix-state.json` (repo-local): write
  `{branch, issue, flags, diagnosis, completed_stages: []}` after each stage; on invocation,
  if it exists and matches the current branch, offer to resume from the next stage (under
  `--yolo`, resume automatically without asking); delete it on success. `.fix-state.json`
  tracks only Stages 0–3 — Stage 4 is `ship`, which keeps its **own** `.ship-state.json`; on a
  resume that lands in Stage 4, hand to `ship` and let it resume its own sub-state rather than
  adding a second resume prompt.

## Stage 0 — Preflight

1. Parse flags and capture the issue text. Read state file → offer resume if it matches (under
   `--yolo`, resume automatically — don't ask).
2. `git status`. If the tree is dirty with unrelated work, surface it — the fix should land on
   a clean base. Under `--yolo`, stash/branch around it rather than asking.
3. **Resolve the base branch** this fix will target — a host/worktree tool's recorded target
   if there is one, else the repo default (`git remote show origin` / `origin/HEAD`) — to name
   the branch. `ship` re-resolves the base authoritatively at its own Stage 0, so this is only
   to inform branch creation, not a value `ship` reads back.

## Stage 1 — Triage (diagnose)

Run the `triage` skill on the issue. It fans sub-agents across the angles (reproduce, recent
changes, backward root-cause trace, pattern/blast-radius), adversarially verifies the leading
hypothesis, and returns a **diagnosis + recommended fix** — it changes no code.

**Gate:** if triage cannot reach a root cause backed by evidence → STOP and report the
diagnosis-so-far and what's still unknown. Do not proceed to implement a guess. Record the
diagnosis in the state file.

## Stage 2 — Branch

Create a working branch named `fix/<kebab-slug>` (slug derived from the diagnosis) **before**
editing anything. If already on a suitable non-default branch, reuse it; never implement on
`main`/`master`.

## Stage 3 — Implement the fix

Apply triage's recommended fix, carrying its discipline:

- **Failing test first**, where the repo has a test harness: the smallest reproduction,
  red *for the bug's reason* before the fix, green after — so it can't silently stop guarding
  the behavior later.
- **Fix at the root cause, not the symptom.** Smallest correct change; no "while I'm here"
  refactors (those are `simplify`/`code-review`'s job inside `ship`).
- Consider **defense-in-depth** only where the bug warrants it (see triage's
  `defense-in-depth.md`) — don't over-apply.

Leave broader cleanup, review, and commit to `ship` — don't pre-empt its stages here.

## Stage 4 — Ship

Hand off to the `ship` skill, passing through `--yolo` / `--merge` / `--no-monitor` / `--fast` /
`--no-verify`.
`ship` runs the full pipeline (simplify → verify → code-review → smart-commit → branch
hygiene → PR → babysit → reflect) and owns its own checkpoint and end-state. Don't duplicate
any of its stages here — `fix`'s job ends by delegating to it.

- Under `--yolo`, `ship`'s Stage 6 checkpoint auto-confirms (hands-off to a green PR); merge
  still requires `--merge`. `ship`'s final Stage 10 (`reflect`) self-gates and, on a hands-off
  run, only *surfaces* any knowledge suggestions without blocking — it never auto-writes, so
  the run still completes without a human reply.
- Without `--yolo`, `ship`'s single checkpoint is the one human pause for the whole `fix` run.

## End state

Delete `.fix-state.json` on success. The final summary chains triage's diagnosis (symptom →
root cause → fix) with `ship`'s end-state (PR #N green and mergeable: <url>, or merged under
`--merge`) — every stage listed as run / skipped (--flag) / halted, no silent gaps.
