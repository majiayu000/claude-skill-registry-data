---
name: qa
description: Run the E2E QA test suite against the live application using Playwright MCP and nREPL. Use when testing the app end-to-end.
argument-hint: "[script-number | 'all' | 'next' | 'status']"
---

# E2E QA Runner

Execute the structured QA test scripts in `qa/scripts/` against the live application.

## Current Progress

!`cat qa/scripts/progress.md`

## How It Works

The QA suite is split into individually-executable test scripts in `qa/scripts/`. Each script:
- Targets a specific feature area (e.g., "Auth Flow", "Core Pages")
- Contains step-by-step TEST items tagged as READ, WRITE, NAVIGATE, or GUARD
- Requires mandatory SCREENSHOT proof at state transitions
- Tracks pass/fail per item

## Invocation

- `/qa` or `/qa next` -- Run the next incomplete script (first `--` status in progress.md)
- `/qa all` -- Run all scripts from the beginning (Session 1 through end)
- `/qa 03` or `/qa 3` -- Run a specific script by number (e.g., `03-feature.md`)
- `/qa status` -- Show current progress.md without running anything
- `/qa 03-08` -- Run a range of scripts sequentially

## Execution Protocol

**Before running any script**, read and internalize the rules in `qa/scripts/EXECUTION-RULES.md`. These are non-negotiable:

1. **Execute EVERY test item in order.** Do NOT skip. Do NOT reorder.
2. **Do NOT move to the next TEST until the current TEST is fully verified.**
3. **"Page loads" is NOT "feature works."** If a test says WRITE, perform the write.
4. **Take a SCREENSHOT at every SCREENSHOT marker.** These are mandatory proof-of-work.
5. **If a test FAILS, log the failure and continue.** Do NOT silently skip. Do NOT fix bugs mid-QA.
6. **When a script completes, update `qa/scripts/progress.md`** with pass/fail/skip counts.
7. **If you cannot finish a script, STOP at the nearest `---` break.** Update progress.md as PARTIAL. Do NOT rush remaining items.

## Steps

### 1. Determine which script(s) to run

Parse `$ARGUMENTS`:
- `next` or empty: Read `qa/scripts/progress.md`, find the first row with Status `--`, that's the script to run.
- `all`: Start from script 00.
- A number (e.g., `3`, `03`, `15`): Run that specific script. Zero-pad to 2 digits to find the file.
- A range (e.g., `03-08`): Run scripts 03 through 08 sequentially.
- `status`: Print progress.md and stop.

### 2. Prerequisites check (Script 00)

If running script 00, or if this is the first script in a session:
1. Connect to nREPL via `/nrepl-connect`
2. Check if the system is running: `(some? repl-stuff/service)`
3. If not running, do a clean start:
   - `rm -rf storage/cache`
   - Eval the start form from `development/src/repl_stuff.clj`
4. Seed: `(require 'e2e-seed :reload) (e2e-seed/seed! repl-stuff/context)`
5. Verify seed output mentions expected counts

If the system is already running and seeded (script 00 shows completed in progress.md), skip to step 3.

### 3. Execute the script

1. Read the script file: `qa/scripts/{NN}-{name}.md`
2. Read the execution rules: `qa/scripts/EXECUTION-RULES.md`
3. Log in as the role specified in the script header
4. Execute each TEST item sequentially:
   - For **NAVIGATE**: Use `browser_navigate` or `browser_click`, verify URL/page title
   - For **READ**: Use `browser_snapshot` and verify expected elements/text
   - For **WRITE**: Perform the action (fill form, click button), then verify the result
   - For **GUARD**: Attempt the blocked action, verify error/redirect
   - At **SCREENSHOT** markers: Use `browser_take_screenshot` with the specified filename
5. Track results: count passes, failures, and skips

### 4. Record results

After completing the script, append the results section to the script file:

```markdown
---
## Results
**Date**: [today's date]
**Status**: PASS | PARTIAL | FAIL
**Pass**: X / Y
**Failures**:
- TEST X.Y: [description]
**Notes**: [anything relevant]
```

Then update `qa/scripts/progress.md` -- change the row's Status, Pass, Fail, Skip, and Date columns.

### 5. Continue or stop

- If running a range or `all`: proceed to the next script.
- If the current script took a long time: stop and report. Do NOT rush the next script.
- Always prefer quality over quantity. One thoroughly-tested script is worth more than three skimmed scripts.

## Key Tools

- **Playwright MCP**: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_take_screenshot`, `browser_press_key`, `browser_wait_for`
- **nREPL MCP**: `mcp__nrepl__eval_form` for data verification and seeding
- **Bash**: `curl` for webhook testing, `rm -rf storage/cache` for clean restart

## Adding New QA Scripts

When a new feature is built, add a test script:
1. Create `qa/scripts/{NN}-{feature-name}.md` following the format in existing scripts
2. Add a row to `qa/scripts/progress.md`
3. Add to `qa/scripts/RUN-ORDER.md` in the appropriate session
4. Include: TEST items with (READ/WRITE/NAVIGATE/GUARD) tags, SCREENSHOT markers, clear VERIFY criteria
