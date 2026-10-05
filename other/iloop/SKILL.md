---
name: iloop
description: "In-session iterative loop — keeps Claude running in the current session until a task is done. Unlike /loop (which spawns background workers), /iloop stays in the current session and re-prompts each iteration via Stop hook. Use for: 'keep fixing until tests pass', 'iterate until this feature works', autonomous debugging. Triggers on: '/iloop', 'in-session loop', 'keep iterating', 'loop until done'."
argument-hint: '"task description" [--max-iterations N] [--completion-promise "TEXT"]'
user_invocable: true
---

# iloop — In-Session Iterative Loop

Runs Claude in a self-contained loop within the **current session** — no background processes, no worktrees. Each iteration, Claude reads the last output, checks progress, makes changes, and verifies. The loop continues until the task is done or max iterations is reached.

## How it works

```
User: /iloop "Fix all failing tests"
          ↓
Claude starts → works on task → tries to exit
          ↓
Stop hook detects .claude/iloop.local.md
          ↓
Feeds task prompt back → Claude continues
          ↓
Repeat until: <promise>DONE</promise> | <loop-abort> | max iterations
```

This is different from `/loop` (which uses background workers + worktrees). Use `/iloop` when:
- You want to stay in the current session and watch progress
- The task needs iterative self-correction within one context
- You want Claude to autonomously debug/fix until passing

## Usage

```
/iloop "Fix all failing pytest tests"
/iloop "Implement the auth feature" --max-iterations 25
/iloop "Get CI green" --completion-promise "ALL TESTS PASSING" --max-iterations 30
```

## Signals (output anywhere in response to control the loop)

| Signal | Effect |
|--------|--------|
| `<loop-abort>reason</loop-abort>` | Terminate immediately (e.g. impossible task, needs human decision) |
| `<loop-pause>what needed</loop-pause>` | Pause — state saved, resume by reopening session |
| `<promise>TEXT</promise>` | Signal completion (only when `--completion-promise` set and genuinely true) |

## Startup

When `/iloop` is invoked:

**Step 1:** Run the setup script:
```bash
bash ~/.claude/scripts/setup-iloop.sh "$ARGUMENTS" --max-iterations 20 --completion-promise "LOOP_DONE"
```

Adjust `--max-iterations` and `--completion-promise` based on the task:
- Simple fix: 10-15 iterations
- Feature build: 25-30 iterations
- Open-ended improvement: omit `--completion-promise`, use `--max-iterations`

**Step 2:** Tell the user:
```
▸ iloop started — iterating until done (max 20 iterations)
▸ Cancel: rm .claude/iloop.local.md
▸ Monitor: head -8 .claude/iloop.local.md
```

**Step 3:** Begin working on the task immediately. Per-iteration protocol:
1. Read git log and key files to understand what was done last iteration
2. Run verification (tests / build / lint) to check current state
3. Make focused progress — fix one thing at a time, not multiple things
4. Run verification again after changes — evidence required before marking done
5. Scan for related issues (fix A → check B and C)
6. Only output `<promise>LOOP_DONE</promise>` when ALL criteria are genuinely met

## Cancelling

```bash
rm .claude/iloop.local.md    # Immediate cancel
```

Or output `<loop-abort>reason</loop-abort>` from within the session.

## Difference from /loop

| | `/loop` | `/iloop` |
|--|---------|----------|
| Execution | Background process, parallel workers | Current session, sequential |
| Worktrees | Yes, isolated per worker | No, works on main tree |
| Visibility | Progress via `--status` | Real-time in session |
| Use case | Large parallel improvements | Focused iterative fixing |
| Context | Each worker starts fresh | Same context across iterations |
