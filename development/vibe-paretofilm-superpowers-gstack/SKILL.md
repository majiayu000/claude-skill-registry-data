---
name: vibe
description: Build one feature end to end under the vibe contract — one intake round, locked acceptance tests as the only checkpoint, a fresh subagent per phase, one review, landing.
---

# Vibe: one feature, intake to landing

Invoke with: `/superpowers-gstack:vibe <what to build>`

The user answers questions once, reads the acceptance tests once, and reviews the
finished work once. Everything between is yours to decide and log. The rules live in
the project's CLAUDE.md section **Vibe contract** (marker `gstack-vibe-v1`); this skill
is the procedure. If `.gstack/workflow` is not `vibe`, say so in one line of the intake
(the contract's standing approvals then hold for this invocation only) and suggest
`/superpowers-gstack:adapt` to choose the profile for good.

Begin every Bash call that needs the lock script with:

```bash
SKILL_DIR='<the base directory the Skill tool printed when this skill loaded>'
LOCK="$SKILL_DIR/../../scripts/lock-acceptance-tests.py"
[ -f "$LOCK" ] || LOCK=$(ls ~/.claude/plugins/cache/*/superpowers-gstack/*/scripts/lock-acceptance-tests.py 2>/dev/null | sort -V | tail -1)
[ -f "$LOCK" ] || { echo "BLOCKED — lock-acceptance-tests.py not found; run /plugin update superpowers-gstack"; exit 2; }
```

## Step 0: Read before asking

Load the project's context skill (`.claude/skills/*-context` or `*-kontekst`) if there
is one, then the code the feature touches. Classify the scope: files, tracks, whether
the result is visual (UI, render, video), and the risk tier
`scripts/classify-change.py` would give it. Steps 0–2 change no code. Do not enter plan
mode yourself: leaving it asks the user a second time, and the acceptance tests are the
one checkpoint.

## Step 1: Intake — one round

Ask everything in one `AskUserQuestion` round: at most eight questions, four per call,
recommended option first and marked `(Recommended)`. Always ask for:
- the reference ("fasit") and the 5–10 acceptance criteria you drew from the request,
  so the user can correct them;
- what is out of scope.

Ask nothing you can find in the code, the context skill or CLAUDE.md. After this round,
design, spec and plan are pre-approved.

## Step 2: SPEC.md and PLAN.md

Write `docs/superpowers/vibe/<YYYY-MM-DD>-<feature>/SPEC.md` (goal, non-goals,
acceptance criteria) and `PLAN.md` (small tasks; each has one test and one
"done when" line; no code). Commit both. Do not wait for a spec or plan review.

## Step 3: Acceptance tests — the one checkpoint

Write the acceptance tests from the criteria, in a directory of their own (for example
`Tests/Acceptance/` or `tests/acceptance/`). For visual work the test is a truth check
against the reference — a screenshot or render measured against it — not only unit
tests. Then send ONE message: a short overview that lists the exact files (test name, what it
checks — the user approves an overview, but `lock` commits what is on disk), and this
line for the user to paste:

```
/goal All tasks in PLAN.md are done: tests green, build without warnings, STATUS.md updated. Or stop after 60 turns.
```

`/goal` is started by the user; without it, continue with step 4 when they say ok.
After their ok, lock the tests:

```bash
python3 "$LOCK" lock --feature <feature> --path '<acceptance-test glob>'
```

From here on, never edit a locked test to turn red into green, by any tool. If a test
is wrong, stop and say which one and why; only the user unlocks
(`python3 "$LOCK" unlock --feature <feature>`). Send the lock commit SHA the script
printed in your next message, so the user can check what was locked.

## Step 4: One fresh subagent per phase

Run the phases of PLAN.md with `superpowers:subagent-driven-development`: each phase's
part of the plan is one subagent's brief; the main thread orchestrates and stays under
about 150k tokens of context. Two fixed rules go into every brief:
- **wire what you build into the app in the same round** the tests turn green — green
  tests on code nothing calls are not done;
- **find every place the app already does the same job** and make it follow the new
  rules.

At every phase boundary update `STATUS.md` (done, remaining, open Rulings). Add one line
per round to `ROUNDS.md`: what was tried, which tests still failed. Never ask "what
next" between phases.

**Stop only for:** irreversible or destructive actions, security-sensitive actions,
side effects outside the worktree, a force-push or a push to the default branch outside
the `Landing mode:` line, money, a licence, or a real blocker. Pushing the feature branch
for backup is pre-approved. Decide everything else and log it in STATUS.md as
`Ruling: <choice> — <why> — <cost if wrong>`.

## Step 5: Tests while working

A subagent runs only the tests that cover what it changed (the affected target or a
`--filter`). The full suite runs at each phase boundary and once before landing.
After a timeout: at most two reruns, then one single run with its log.

## Step 6: One review, at the end

Invoke `/superpowers-gstack:pitfall-verification` once, after the last phase, on the
whole branch; its tier is computed as always. Fix critical and important findings; do
not re-review minor ones. No plan reviews, no `/autoplan`.

## Step 7: Lessons, committed before landing

Read `ROUNDS.md`: a mistake that came back in two phases or more becomes one working
rule — at most three per feature — in the **How we work** section of the context skill,
never into CLAUDE.md. Commit the change now, on the feature branch: lessons written
after landing never reach the default branch and vanish with the worktree. Touch neither
the locked tests nor the contract in this step.

## Step 8: The lock must hold

```bash
python3 "$LOCK" verify --feature <feature>
```

Exit 0 is required before landing. Exit 1 names each changed file (the receipt
`.gstack/acceptance-lock.json`, a new file under a locked path and a hidden
assume-unchanged flag included): restore it from the lock commit, or stop and tell the
user which test is wrong. The lock defends against mistakes and shortcuts, not against deliberate history
rewriting; `verify` is a gate, not proof. It compares the locked files with the lock
commit in the working tree, the index and HEAD, and checks the receipt and new files
under the locked paths. It cannot see a `conftest.py` or pytest configuration outside
those paths that changes what the tests do, a faked or amended commit subject on the
receipt, or a rewritten history. After a rebase it warns that the lock commit left the
branch's history: tell the user, who can re-lock. In `pr` landing mode, when another
feature's squash-merge commit changed the receipt on main, `verify` exits 1 ("receipt
changed by commit …") after a rebase: re-lock. Only `__pycache__`, `.pytest_cache` and
`.DS_Store` are exempt from the new-file check.

## Step 9: Land

Land by the project's `Landing mode:` line — `solo` → `/superpowers-gstack:land`,
`pr` → `/ship` — with no options menu. Ask once about the push only when the project
requires it. The lock stays after landing as the record: the landed tests remain
protected, and only the user unlocks them.

## Step 10: Final report

One message: what was built, how the user verifies it, every Ruling, deferred findings.
