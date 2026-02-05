---
name: web-test-cleanup
description: Clean up test sessions - kill browsers, stop dev servers, free ports, and optionally remove test data. Use this BEFORE starting new tests or AFTER completing tests.
license: MIT
compatibility: Node.js 18+
metadata:
  author: AI Agent
  version: 1.0.0
allowed-tools: Bash Read
---

# Test Cleanup

Clean up test sessions by closing browsers, stopping dev servers, freeing ports, and optionally removing test data.

## When to Use This Skill

- **BEFORE starting new tests** - Run without `--keep-data` to get a clean slate
- **AFTER completing tests** - Run with `--keep-data` to preserve test artifacts for review
- **When tests are stuck** - Kill hanging browser or server processes
- **When ports are blocked** - Free common dev ports (3000, 5173, 8080, 4200, 4321)

## Quick Start

```bash
SKILL_DIR="<path-to-this-skill>"

# Full cleanup (removes test-output folder)
$SKILL_DIR/scripts/cleanup.sh

# Keep test data (screenshots, wallet config, etc.)
$SKILL_DIR/scripts/cleanup.sh --keep-data
```

## What Gets Cleaned Up

### Dev Server Stopped
- Reads `test-output/.dev-server.json` to find and stop the dev server process started by web-test
- Only kills the specific process we started, NOT other processes on common ports

### Processes Killed
- Test browser processes (Chrome/Chromium using test-output profile)
- Browsers using remote-debugging-port 9222

### Ports Freed
- The port used by our dev server (as recorded in `.dev-server.json`)
- Does NOT kill other processes on common ports to avoid affecting unrelated services

### State Files Cleaned
- `.browser-cdp.json` - Browser CDP connection info
- `.browser-state.json` - Browser state
- `.dev-server.json` - Dev server process info

### Files Removed (unless `--keep-data`)
```
<project-root>/test-output/
├── screenshots/                      # Test screenshots
├── chrome-profile/                   # Browser state, wallet data
├── extensions/                       # Downloaded wallet extensions
├── console-logs.txt                  # Browser console output
└── test-report-YYYYMMDD-HHMMSS.md    # Generated test report (timestamped)
```

## Instructions

### Pre-Test Cleanup (Fresh Start)

Before starting a new test session, run full cleanup:

```bash
SKILL_DIR="<path-to-this-skill>"

# Kill all processes and remove test data
$SKILL_DIR/scripts/cleanup.sh
```

This ensures:
- No stale browser windows interfering with tests
- No blocked ports preventing server startup
- Clean test-output folder for new artifacts

### Post-Test Cleanup (Preserve Data)

After completing tests, run cleanup with `--keep-data`:

```bash
SKILL_DIR="<path-to-this-skill>"

# Kill processes but keep test artifacts
$SKILL_DIR/scripts/cleanup.sh --keep-data
```

This:
- Closes all browser windows
- Stops dev servers
- Preserves screenshots and reports for review
- Keeps wallet configuration for future tests

## Manual Cleanup Commands

If the cleanup script is not available, you can run these commands manually:

```bash
# Stop dev server using saved PID (only kills our process)
DEV_PID=$(node -e "console.log(require('./test-output/.dev-server.json').pid)" 2>/dev/null)
kill -9 $DEV_PID 2>/dev/null

# Kill browser processes (only test browsers)
pkill -f "Google Chrome.*test-output"
pkill -f "chromium.*test-output"
pkill -f "remote-debugging-port=9222"

# Remove state files
rm -f ./test-output/.dev-server.json
rm -f ./test-output/.browser-cdp.json
rm -f ./test-output/.browser-state.json

# Remove test data
rm -rf ./test-output/
```

## Exit Codes

- `0` - Cleanup completed successfully
- `1` - Cleanup failed (check error message)

## Notes

- Always run cleanup before starting new test sessions
- Use `--keep-data` when you need to review test results
- The cleanup script is in this skill's `scripts/` directory
- Test data is stored in the project directory, not the skill directory
