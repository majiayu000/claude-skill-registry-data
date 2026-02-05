---
name: task-debugger
description: |
  Debug and fix failures in Taskcluster tasks. Use this skill when the user asks to debug a task, fix a failing task, or investigate task errors/failures. This skill uses the Taskcluster CLI to fetch task logs and definitions, analyzes errors, and uses `taskgraph load-task --develop` to reproduce and debug issues locally. Invoke this for any request involving Taskcluster task debugging, task failures, or when given a task ID to investigate.
---

# Task Debugger Skill

You are a Taskcluster task debugging expert. Your goal is to identify and fix failures in Taskcluster tasks by using `taskgraph load-task --develop` to reproduce and debug issues locally.

## When to Use This Skill

This skill should be invoked when the user asks to:
- Debug a task (e.g., "Figure out what's wrong with task <task-id>")
- Fix a failing task (e.g., "Fix the failure in <task-id>")
- Investigate task errors or failures

## Required Tool: Taskcluster CLI

The Taskcluster CLI client is essential for debugging tasks. It provides commands to fetch task definitions, logs, and status information.

### Installation

**Check if already installed:**
```bash
taskcluster --version
```

**If not installed, install it:**

For Linux (download latest release):
```bash
curl -L https://github.com/taskcluster/taskcluster/releases/latest/download/taskcluster-linux-amd64 -o /tmp/taskcluster
chmod +x /tmp/taskcluster
sudo mv /tmp/taskcluster /usr/local/bin/taskcluster
```

For macOS:
```bash
brew install taskcluster/tap/taskcluster
```

### Configuration

Set the Taskcluster root URL for Firefox CI:
```bash
export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com
```

**Note:** You don't need authentication credentials for read-only operations like fetching task logs and definitions.

### Useful Commands

- `taskcluster task log <task-id>` - Fetch and stream task logs
- `taskcluster task def <task-id>` - Get the full task definition (JSON)
- `taskcluster task status <task-id>` - Check task status
- `taskcluster help` - Show all available commands

## Workflow

### 1. Setup Taskcluster CLI

First, ensure the Taskcluster CLI is installed and configured:

```bash
# Check if installed
taskcluster --version

# If not, install it (see Installation section above)

# Configure for Firefox CI
export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com
```

### 2. Extract Task Information

From the user's message, extract the task ID. Task IDs conform to this regex pattern:
```
^[A-Za-z0-9_-]{8}[Q-T][A-Za-z0-9_-][CGKOSWaeimquy26-][A-Za-z0-9_-]{10}[AQgw]$
```

If the user provides a Taskcluster URL instead, extract the task ID from it:
- Format: `https://firefox-ci-tc.services.mozilla.com/tasks/<task-id>`

### 3. Fetch Task Information

Use the Taskcluster CLI to gather information about the failing task:

**Fetch task logs:**
```bash
taskcluster task log <task-id>
```

This will stream the complete task log. Look for error messages, tracebacks, and failure indicators.

**Optional - Fetch task definition:**
```bash
taskcluster task def <task-id>
```

The task definition is useful for understanding:
- What command is being run (`payload.command`)
- Environment variables (`payload.env`)
- Docker image being used (`payload.image`)
- Required caches or volumes
- Task dependencies

**Check task status:**
```bash
taskcluster task status <task-id>
```

This shows the current state and run information.

### 4. Analyze the Error

After fetching the logs:
1. Identify the root cause of the failure
2. Look for:
   - Python tracebacks
   - Test failures
   - Build errors
   - Missing dependencies
   - Environment issues
   - Command failures

### 5. Determine Fix Strategy

**If the solution is obvious** (e.g., syntax error, import error, simple logic bug):
- Make the fix directly
- Proceed to verification (step 6)

**If the solution is NOT obvious**:
- Add print/debug statements to relevant files
- Use `taskgraph load-task --develop <task-id>` to run the task locally with your changes
- Review the new debug output
- Iterate: add more debugging, make fixes, re-run
- Continue until the root cause is identified and fixed

### 6. Verify the Fix

Once you've identified and implemented a fix:

Run the task locally to verify:
```bash
taskgraph load-task <task-id>
```

**Important flags you may need:**
- `--develop`: Use local source at current revision (essential for testing changes)
- `--interactive` / `-i`: Pause before task execution to inspect the environment
- `--volume` / `-v`: Mount additional local paths (format: `HOST_DIR:CONTAINER_DIR`)
- `--root` / `-r`: Specify relative path to taskgraph definition root
- `--image`: Override task image with custom image, `task-id=<id>`, or `index=<path>`
- `--keep`: Keep container after exit for post-mortem debugging
- `--user`: Specify container user

**Typical verification command:**
```bash
taskgraph load-task --develop <task-id>
```

The task should complete successfully if your fix works.

### 7. Clean Up

**Critical:** Before finishing, remove all debugging artifacts:
- Delete or comment out any print/debug statements you added
- Remove any temporary debugging scripts
- Ensure the code is clean and production-ready

**Important:** Do NOT re-run verification after cleanup. Trust that your fix works based on the previous successful run.

### 8. Report Results

Provide the user with:
1. **Root cause**: Explain what was causing the failure
2. **Fix applied**: Describe the changes you made
3. **Verification**: Confirm the task now passes locally
4. **Files changed**: List the files you modified

## Tips and Best Practices

### Using the Taskcluster CLI Effectively

- Use `taskcluster task log <task-id>` to see the full task output
- Use `taskcluster task def <task-id>` to inspect the task configuration
- The task definition JSON shows exactly what command runs, what env vars are set, and what image is used
- Task logs are streamed in real-time, so you see output as it would appear in CI

### Common Taskcluster Task Patterns

- Tasks often use `run-task` script for execution
- Look for `command` field in task definition for what actually runs
- Environment variables are critical - check `env` section
- Artifacts are typically under `public/` paths

### Debugging Strategies

1. **Start broad, narrow down**: Use print statements to trace execution flow
2. **Check environment**: Verify environment variables, paths, and dependencies
3. **Compare with passing tasks**: If similar tasks pass, diff their definitions
4. **Read error messages carefully**: The actual error is often at the END of a traceback
5. **Check recent changes**: Failures often correlate with recent commits

### Using `--develop` Effectively

The `--develop` flag is your most powerful tool:
- It uses your LOCAL source at the CURRENT revision
- You can make changes and immediately test them
- No need to push commits or create CI tasks
- Faster iteration cycle

### Common Gotchas

- Make sure Docker is running before using `load-task`
- Some tasks require specific caches or volumes - check task definition
- Network issues can cause transient failures - not all failures are code bugs
- Some tasks have dependencies on other tasks - check if prerequisites succeeded

## Example Interaction Flow

```
User: "Figure out what's wrong with task ABC123XYZ"

1. Setup: Check `taskcluster --version`, set TASKCLUSTER_ROOT_URL
2. Fetch logs: `taskcluster task log ABC123XYZ`
3. Analyze: "ImportError: cannot import name 'foo' from 'bar'"
4. Fix: Add missing import to bar/__init__.py
5. Verify: Run `taskgraph load-task --develop ABC123XYZ`
6. Success: Task completes without errors
7. Clean up: No debug statements were added, so nothing to clean
8. Report: "Fixed missing import in bar/__init__.py:15. Task now passes locally."
```

## Remember

- Always use `--develop` when verifying fixes (so local changes are used)
- Clean up ALL debugging artifacts before finishing
- Don't re-verify after cleanup
- Be methodical and thorough in your investigation
- Document what you found and what you changed

Now proceed with debugging the task based on the user's request!
