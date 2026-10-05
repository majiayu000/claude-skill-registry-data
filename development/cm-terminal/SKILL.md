---
name: cm-terminal
description: Use when running ANY terminal command - enforces clear progress logging, output reading, and error-stop behavior so terminal processes are never left unchecked
---

# Terminal Process Monitoring

## Overview

Running commands without checking output is flying blind. Users MUST see what's happening at every step.

**Core principle:** Every command gets announced, monitored, and verified. No exceptions.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMMAND RUNS WITHOUT READING ITS OUTPUT.
NO ERROR GOES UNREPORTED.
NO NEXT STEP WITHOUT PREVIOUS STEP CONFIRMED.
```

## When to Use

**ALWAYS** when running terminal commands via `run_command`. This includes:
- Build commands (`npm run build`, `npm run dev`)
- Test commands (`npx vitest run`)
- Install commands (`npm install`)
- Deploy commands (`npx wrangler pages deploy`)
- Git commands (`git push`, `git commit`)
- Any script or CLI tool

## The Protocol

### Step 1: Announce Before Running

**BEFORE calling `run_command`:**

Update `task_boundary` TaskStatus to describe what you're about to run and why.

```
TaskStatus: "Running npm build to compile production bundle"
TaskStatus: "Installing dependencies with npm install"
TaskStatus: "Deploying to Cloudflare Pages"
```

### Step 2: Set Appropriate Wait Time

Choose `WaitMsBeforeAsync` based on expected command duration:

| Command Type | WaitMsBeforeAsync | Strategy |
|-------------|-------------------|----------|
| Quick (< 3s) — `git status`, `ls`, `cat` | 3000-5000 | Synchronous, read output directly |
| Medium (3-30s) — `npm install`, `build` | 5000-10000 | Wait for initial output, then poll |
| Long (> 30s) — `deploy`, `test suites` | 2000-5000 | Send to background, poll actively |

### Step 3: Read Output Immediately

**After `run_command` returns:**

1. If command completed synchronously → read output in the response
2. If command sent to background → call `command_status` immediately with `WaitDurationSeconds: 10`
3. **NEVER proceed to next step without reading output**

### Step 4: Check for Errors

Scan output for error indicators:

```
ERROR PATTERNS TO DETECT:
- Exit code ≠ 0
- "error", "Error", "ERROR"
- "fail", "FAIL", "failed", "FAILED"
- "ENOENT", "EACCES", "EPERM"
- "not found", "No such file"
- "Cannot find module"
- "SyntaxError", "TypeError", "ReferenceError"
- "Build failed"
- "Command failed"
- "Permission denied"
- "FATAL"
- Stack traces (lines with "at " prefix)
- npm ERR!
- Warning patterns that indicate real problems
```

### Step 4b: Compress Before Quoting

**Before pasting stdout into TaskSummary or model context:**

| Command pattern | Rule |
|-----------------|------|
| `git status` | Keep only changed entries + branch line + `(N changed)` count. Drop "use git add…" boilerplate. |
| `npm test` / `vitest` / `jest` | Keep failing tests + summary line. Drop `PASS` lines. |
| `npm run build` / `tsc` | Keep `error` / `warning` / final status. Drop incremental progress. |
| Any output | Collapse runs of ≥ 3 identical lines into `<line>  … (× N)`. |

**Helper:** `src/utils/output-compress.ts` — `compressGitStatus`, `compressNpmTest`, `summarizeBuildLog`, `collapseRepeatedLines`, `compressFor(command, stdout)`.

**Anti-pattern:** Pasting full stdout (> 50 lines) into TaskSummary when only the failing portion matters. Compress first, then quote.

### Step 5: Stop on Error

**If ANY error is detected:**

```
1. STOP — Do not run any more commands
2. IDENTIFY — Extract the exact error message and context
3. REPORT — Call notify_user with error if critical
4. FIX — Use cm-debugging if proceeding to fix
```

### Step 6: Poll Long-Running Commands

**For background commands (returned a CommandId):**

1. Poll `command_status` every 10-15 seconds
2. After EACH poll, update `task_boundary` TaskStatus with latest output summary
3. Continue until command completes (status: "done")
4. Read final output and check for errors

### Step 7: Confirm Success

**Only after reading output AND confirming no errors:**

Update `task_boundary` TaskSummary with the result:
```
TaskSummary: "Build completed successfully (0 errors, 0 warnings)"
TaskSummary: "All 519 tests passed"
TaskSummary: "Deployed to https://prms-4pv.pages.dev successfully"
```

## Red Flags — STOP and Follow Protocol

If you catch yourself doing ANY of these:

- Running a command without updating TaskStatus first
- Calling `run_command` while previous command is still running
- Skipping `command_status` for a background command
- Proceeding to next step without reading output
- Ignoring warnings or errors in output
- Assuming a command succeeded without checking exit code
- Running 3+ commands in parallel without monitoring each

**ALL of these mean: STOP. Follow the protocol.**

## Anti-Patterns

| DON'T | DO |
|-------|-----|
| Run and forget | Run and read output |
| Assume success | Verify success from output |
| Chain commands blindly | Verify each before next |
| Ignore warnings | Report warnings to user |
| Multiple commands without checking | Sequential with verification |

## Special Cases

### Interactive Commands (dev servers, watch mode)

1. Start with `WaitMsBeforeAsync: 3000-5000`
2. Check initial output for startup success/failure
3. Look for "ready" / "listening on" / "compiled successfully" signals
4. Report the URL/port to user
5. Note the CommandId for future reference

### Parallel Commands

If running multiple commands at once:
1. Track ALL CommandIds
2. Poll each one separately
3. If ANY fails → report which one failed

### Piped/Chained Commands (`&&`, `|`)

1. The exit code reflects the LAST command in the chain
2. Read full output — errors from earlier commands may appear but the chain continues
3. Be extra careful with `cd dir && npm run build` — if `cd` fails, build won't run

## Severity Levels

| Level | Action | Example |
|-------|--------|---------|
| 🟢 **Success** | Update TaskSummary, proceed | "Build succeeded" |
| 🟡 **Warning** | Report to user, ask if proceed | "Deprecated dependency" |
| 🔴 **Error** | STOP immediately, notify_user or fix | "Build failed", "Test failed" |
| ⚫ **Fatal** | STOP immediately, notify_user | "ENOENT", "Permission denied" |

## The Bottom Line

**Every command tells a story through its output. READ the story. SHARE it with the user. STOP if the story is bad.**
