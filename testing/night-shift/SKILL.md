---
name: night-shift
description: Use this skill whenever the user wants to set up an overnight autonomous build, ship while they sleep, run agents overnight, prepare for an autonomous loop, or review overnight work. Also trigger when the user says "I want the agent to work while I sleep", "set up a night run", "prepare for overnight build", "check what happened overnight", "review overnight work", or "did the overnight build succeed?" Use this skill to prepare pre-sleep checklists and do morning reviews — the actual autonomous loop is handled by Ralph or Claude Code's native loop features, which this skill configures and wraps.
---

# Night Shift

Help the user run autonomous overnight builds safely and review the results in the morning.

## Overview

This skill has two modes. Figure out which one based on context:

- **PREPARE mode**: Pre-sleep. The user wants to set up an autonomous run before going to bed. Generate the pre-flight check, configure guardrails, and hand off to Ralph (or Claude Code's loop feature) for the actual overnight execution.
- **REVIEW mode**: Morning. The user wants to check what happened overnight. Analyze git history, verify acceptance criteria, surface anomalies, and generate a summary.

The skill does NOT run the overnight loop itself. That's Ralph's job (or Claude Code's native `/loop` command). This skill handles the human rituals around the loop — preparation and review — which is where most autonomous runs fail when done poorly.

If the user hasn't installed Ralph yet, read `references/ralph-integration.md` and guide them through setup before proceeding.

---

## PREPARE Mode (before bed)

### Step 1: Reality Check

Before anything else, ask the user:

1. How long is this their first overnight run? (If yes, recommend a 1-hour "nap run" first, not 8 hours.)
2. Which specs do they want built overnight? (If more than 3, push back — start smaller.)
3. Is the project committed? (If not, refuse to proceed until it is.)

**Hard rules:**
- If it's the first autonomous run, MAX 1 spec and MAX 2 hours. Period.
- If the git state is dirty, refuse to proceed.
- If tests don't currently pass, refuse to proceed — the agent won't know if it broke something.
- If the specs chosen touch critical auth/payment code, warn the user and require explicit confirmation.

These aren't bureaucratic gates. They're the difference between waking up to shipped work vs. waking up to 8 hours of corrupted code.

### Step 2: Pre-Flight Check

Run `scripts/check_sleep_ready.py`:

```bash
python {baseDir}/scripts/check_sleep_ready.py --specs /specs/spec1.md /specs/spec2.md
```

The script checks:
- Git state is clean (no uncommitted changes)
- Current branch is not `main`/`master` (safer on a feature branch)
- Tests pass (`npm test`, `pytest`, etc. — detected from package.json or similar)
- Typecheck passes (if applicable)
- Specified specs exist and are well-formed (have all 5 sections from Issue 03)
- CI is green (if configured)

The script outputs PASS or BLOCKED with reasons. If BLOCKED, stop and tell the user what to fix.

### Step 3: Generate Guardrails

Read `references/guardrails.md` for the guardrail philosophy, then generate guardrails specific to this run.

Guardrails have three parts:

**Scope guardrails** — what the agent can and cannot touch:
- Allowed directories: only the files mentioned in the spec
- Blocked directories: auth, payments, migrations, CI config (unless the spec is explicitly about these)
- Read-only files: PROJECT.md, SKILL.md files, production env files

**Kill conditions** — when the loop should abort and wake the user:
- Tests fail and can't be fixed in 2 iterations
- Build fails and can't be fixed in 2 iterations
- Agent hits the same error 3 times in a row (stuck loop)
- Agent modifies a file outside the allowed scope
- Agent installs a dependency not in the spec's constraints
- More than 20 files modified (scope creep signal)
- Git history diverges in unexpected ways

**Budget guardrails** — resource limits:
- Max iterations: 10 (start low, increase after trust is built)
- Max wall-clock time: matches the user's actual sleep window
- Max API calls / tokens (if the user has a budget)

### Step 4: Configure the Loop

Convert the user's Issue 03 specs into Ralph's `prd.json` format. Read `references/ralph-integration.md` for the conversion logic.

For each spec:
1. Extract requirements into user stories
2. Map acceptance criteria to `tests` or verification steps
3. Set priority order based on dependencies
4. Add the generated kill conditions to the global config

Save the generated config to `/.night-shift/prd.json` (or Ralph's expected location).

If the user is using Claude Code's native `/loop` feature instead of Ralph, generate the equivalent config for that.

### Step 5: Set Up the Kill Switch

Create a simple kill mechanism the user can trigger if they wake up and need to abort:

```bash
# Generated kill script at /.night-shift/kill.sh
#!/bin/bash
touch /.night-shift/ABORT
echo "Kill signal sent. Loop will stop on next iteration."
```

The Ralph config reads `/.night-shift/ABORT` at the start of each iteration and exits if it exists. Tell the user:

```
KILL SWITCH:
If you wake up and want to stop the run, run:
  bash /.night-shift/kill.sh

The loop will exit cleanly on its next iteration check (within 60 seconds).
```

### Step 6: Final Briefing

Present a summary to the user:

```
NIGHT SHIFT READY

Configuration:
  Specs: 2 (feature-response-analytics, fix-mobile-form)
  Max iterations: 8
  Max runtime: 6 hours (from 11 PM to 5 AM)
  Scope: /app/responses/*, /components/ui/*, /components/mobile/*
  
Blocked areas:
  /app/api/auth/*, /prisma/migrations/*, .env*

Kill conditions:
  • 3 consecutive errors → abort + notify
  • Tests fail twice → abort
  • Scope violation → abort immediately
  • File count > 20 → abort

To start the loop:
  bash /.night-shift/run.sh

To abort while sleeping:
  bash /.night-shift/kill.sh

In the morning:
  Say "review last night's work" and I'll analyze what happened.

Good luck. Go to sleep.
```

Do NOT run the loop automatically. The user clicks the button. The human confirms the launch.

---

## REVIEW Mode (in the morning)

### Step 1: Load the Overnight State

Check for the overnight run artifacts:
- `/.night-shift/prd.json` (what was attempted)
- `/.night-shift/progress.txt` (Ralph's learning log, if used)
- Git log since the night-shift branch was created
- Test results, build results

If any of these are missing or the loop didn't run, ask the user what happened.

### Step 2: Run the Review Script

```bash
python {baseDir}/scripts/morning_review.py --since "8 hours ago"
```

The script analyzes:
- Commits made during the night (count, by time, by scope)
- Files modified (check against allowed scope from PREPARE)
- Tests added/modified and their current pass/fail status
- Any scope violations (files touched outside the allowed list)
- Specs completed vs. attempted vs. failed
- Kill condition triggers (if any)
- Anomalies: rapid repeated commits, circular changes, unusual patterns

The script outputs a structured JSON report.

### Step 3: Categorize the Outcome

Based on the report, classify the night into one of four outcomes:

**Outcome A — SHIPPED ✅**
All specs completed, tests pass, no scope violations, clean commit history. Rare on the first few runs. Celebrate. Deploy (Issue 07).

**Outcome B — PARTIAL ⚠️**
Some specs completed, some didn't. Tests still pass. No scope violations. Review completed work, merge what's good, regenerate specs for what failed. Most common successful outcome.

**Outcome C — STUCK 🔄**
Loop ran but got stuck early. Same error repeated. No real progress. Check `progress.txt` — the agent's notes usually reveal what blocked it. Usually a vague spec or a missing dependency the agent couldn't figure out alone. Fix the spec, try again.

**Outcome D — DRIFTED 🚨**
Agent went off-script. Touched files outside scope. Produced code that doesn't match the spec. RESET. Run `git reset --hard` to the pre-sleep checkpoint. Do not try to salvage individual commits — something went wrong upstream and the whole run is suspect. Figure out what failed in the guardrails and fix it before the next attempt.

### Step 4: Generate the Morning Briefing

Present to the user:

```
OVERNIGHT REPORT: [Outcome type]

SPECS:
  ✅ feature-response-analytics — 8 commits, tests passing
  ⚠️  fix-mobile-form — 3 commits, partial implementation, tests failing
  
TIMELINE:
  11:03 PM — Loop started
  11:45 PM — feature-response-analytics completed
  11:47 PM — Started fix-mobile-form
  01:22 AM — Tests failing, iteration 2
  02:10 AM — Tests failing, iteration 3
  02:10 AM — KILL CONDITION: tests failed twice, aborted
  
FILES MODIFIED (in scope):
  /app/responses/analytics/page.tsx (created)
  /components/ui/chart.tsx (modified)
  /components/mobile/form-layout.tsx (modified)
  /components/mobile/form-layout.test.tsx (modified)
  
FILES MODIFIED (out of scope): none ✅

TESTS:
  Before: 47 passing
  After: 52 passing, 3 failing (in mobile form tests)
  
LEARNINGS FROM AGENT (progress.txt):
  "The mobile form test file expects a prop I'm not sure how to provide..."
  "Attempted fix 2: changed default prop, still failing..."
  "Attempted fix 3: reverted to original, now test passes but feature doesn't render..."

RECOMMENDED NEXT STEPS:
  1. Merge analytics feature (it's clean, ready to deploy)
  2. Revert mobile form changes (the agent got stuck)
  3. Review the spec for fix-mobile-form — it was probably ambiguous about the prop contract
  4. Rewrite the spec with explicit prop definitions, try again tonight

Want me to do the merge and revert now?
```

### Step 5: Execute the Cleanup

Based on the user's confirmation:
- **Merge completed work**: `git cherry-pick` or merge the branch, depending on the strategy
- **Revert failed work**: `git revert` the specific commits or `git reset` to the pre-sleep checkpoint
- **Update specs**: for anything that got stuck, rewrite the spec to remove the ambiguity the agent hit
- **Archive the run**: move `/.night-shift/` artifacts to `/.night-shift/archive/[date]/` for future reference

### Step 6: Lessons for Next Time

After 3-5 overnight runs, the user should have a clearer picture of what works. Update `references/guardrails.md` in their project with learnings:
- Which kinds of specs work well overnight (usually: clear scope, existing patterns)
- Which kinds fail (usually: novel integrations, unclear contracts, shared state)
- What kill conditions need to be tighter or looser
- What the max safe iteration count is for their codebase

---

## Important Principles

- **Start small.** First overnight run is 1 spec for 1 hour. NOT 5 specs for 8 hours. Build trust incrementally.
- **The first run will probably fail.** This is normal. The goal of the first run is to discover what your specific guardrails need, not to ship code.
- **Guardrails matter more than the loop.** Ralph handles the loop well. The risk is unbounded scope or missing kill conditions. The skill's main value is generating good guardrails.
- **Dirty git state = no run.** Never start an overnight loop with uncommitted changes. The pre-sleep checkpoint is your safety net.
- **Dependencies between specs are a red flag overnight.** Parallel specs that might conflict should run during the day with the parallel-build skill, not overnight.
- **The morning review is not optional.** Every overnight run needs human review in the morning, even if it looks successful. Never auto-merge.
- **Never leave this running for days.** Overnight is overnight. 8 hours max. Multi-day autonomous runs belong to frameworks like Paperclip, not this skill.
