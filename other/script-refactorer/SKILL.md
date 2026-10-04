---
license: Apache-2.0
name: script-refactorer
description: |
  Modernizes legacy scripts (bash, Node, Python) by replacing deprecated APIs, adding error handling,
  converting callbacks to async/await, and improving maintainability. Turns brittle one-off scripts
  into reliable, documented tools.
category: Code Quality & Testing
tags:
  - refactoring
  - scripts
  - modernization
  - cleanup
  - maintenance
allowed-tools:
  - Read
  - Bash(*)
  - Glob
  - Grep
  - Write
  - Edit
pairs-with:
  - skill: refactoring-surgeon
    reason: General refactoring principles applied to scripts
  - skill: error-handling-patterns
    reason: Robust error handling is the primary script improvement
  - skill: beautiful-cli-design
    reason: Good CLI ergonomics for script interfaces
  - skill: devops-automator
    reason: Scripts often live inside CI/CD pipelines
---

# Script Refactorer

Modernizes legacy scripts into reliable, maintainable tools. Replaces deprecated patterns,
adds error handling and input validation, converts callback spaghetti to async/await,
and turns undocumented one-off hacks into proper CLI tools.

## Activation Triggers

**Use this skill when:**
- A bash/Node/Python script works but is fragile, undocumented, or hard to modify
- Scripts use deprecated Node.js APIs (e.g., `new Buffer()`, `url.parse()`, `fs.exists()`)
- Callback-heavy Node.js code needs async/await conversion
- Scripts lack error handling and fail silently or with cryptic messages
- A script needs proper CLI argument parsing, help text, and exit codes
- Legacy Python 2 patterns need updating to modern Python 3
- Shell scripts lack `set -euo pipefail` and proper quoting

**Do NOT use this skill for:**
- Rewriting scripts from scratch in a different language (use the appropriate language skill)
- Building new CLI tools (use beautiful-cli-design)
- Large application refactoring (use refactor-architect for planning, refactoring-surgeon for execution)
- Performance optimization of scripts (use performance-profiling)

## Core Capabilities

### 1. Bash Script Modernization

**Before** -- the kind of script that makes you wince:

```bash
#!/bin/bash
# deploy.sh - "works on my machine"

cd /opt/app
git pull
npm install
npm run build
pm2 restart app
echo "done"
```

**After** -- a script you can trust:

```bash
#!/usr/bin/env bash
set -euo pipefail

# deploy.sh — Deploy application with rollback safety
# Usage: deploy.sh [--branch <branch>] [--skip-build] [--dry-run]

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly APP_DIR="/opt/app"
readonly LOG_FILE="/var/log/deploy-$(date +%Y%m%d-%H%M%S).log"

# Defaults
BRANCH="main"
SKIP_BUILD=false
DRY_RUN=false

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Deploy the application from git with rollback safety.

Options:
  --branch <branch>   Branch to deploy (default: main)
  --skip-build        Skip npm install and build steps
  --dry-run           Show what would happen without doing it
  -h, --help          Show this help message

Environment:
  APP_DIR             Application directory (default: /opt/app)
  PM2_APP_NAME        PM2 process name (default: app)
EOF
  exit 0
}

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
die() { log "FATAL: $*" >&2; exit 1; }

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --branch)   BRANCH="${2:?--branch requires a value}"; shift 2 ;;
      --skip-build) SKIP_BUILD=true; shift ;;
      --dry-run)  DRY_RUN=true; shift ;;
      -h|--help)  usage ;;
      *)          die "Unknown option: $1" ;;
    esac
  done
}

preflight_checks() {
  command -v git >/dev/null 2>&1 || die "git is not installed"
  command -v npm >/dev/null 2>&1 || die "npm is not installed"
  command -v pm2 >/dev/null 2>&1 || die "pm2 is not installed"
  [[ -d "$APP_DIR/.git" ]] || die "$APP_DIR is not a git repository"
}

main() {
  parse_args "$@"
  preflight_checks

  local prev_commit
  prev_commit=$(git -C "$APP_DIR" rev-parse HEAD)
  log "Current commit: ${prev_commit:0:8}"
  log "Deploying branch: $BRANCH"

  if $DRY_RUN; then
    log "DRY RUN — would deploy $BRANCH to $APP_DIR"
    exit 0
  fi

  # Capture state for rollback
  trap 'log "Deploy failed. Rolling back to ${prev_commit:0:8}"; git -C "$APP_DIR" checkout "$prev_commit" 2>/dev/null' ERR

  git -C "$APP_DIR" fetch origin "$BRANCH"
  git -C "$APP_DIR" checkout "$BRANCH"
  git -C "$APP_DIR" pull origin "$BRANCH"

  if ! $SKIP_BUILD; then
    log "Installing dependencies..."
    (cd "$APP_DIR" && npm ci --production)
    log "Building..."
    (cd "$APP_DIR" && npm run build)
  fi

  log "Restarting application..."
  pm2 restart "${PM2_APP_NAME:-app}"

  log "Deploy complete: $(git -C "$APP_DIR" rev-parse --short HEAD)"
}

main "$@"
```

**Key transformations:**
- `set -euo pipefail` -- fail on errors, undefined variables, pipe failures
- `#!/usr/bin/env bash` -- portable shebang
- Proper argument parsing with `--help`
- Preflight checks for required commands
- Trap-based rollback on failure
- Logging with timestamps
- Readonly variables for constants
- Quoted variables everywhere (no word-splitting bugs)

### 2. Node.js Deprecated API Replacement

| Deprecated | Replacement | Since |
|------------|-------------|-------|
| `new Buffer(data)` | `Buffer.from(data)` | Node 6 |
| `Buffer(size)` | `Buffer.alloc(size)` | Node 6 |
| `url.parse(str)` | `new URL(str)` | Node 10 |
| `url.resolve(from, to)` | `new URL(to, from).href` | Node 10 |
| `fs.exists(path, cb)` | `fs.access(path)` or `fs.stat(path)` | Node 1 |
| `path.exists()` | `fs.existsSync()` | Node 1 |
| `require('domain')` | `AsyncLocalStorage` | Node 13 |
| `crypto.createCipher()` | `crypto.createCipheriv()` | Node 10 |
| `process.binding()` | N/A (internal only) | Node 10 |
| `util.puts/print/debug` | `console.log/error` | Node 0.12 |
| `sys` module | `util` module | Ancient |
| `querystring.parse()` | `URLSearchParams` | Node 10 |
| `os.tmpDir()` | `os.tmpdir()` | Node 4 |

### 3. Callback to Async/Await Conversion

**Before** -- callback pyramid:

```javascript
const fs = require('fs');
const path = require('path');

function processFiles(dir, callback) {
  fs.readdir(dir, function(err, files) {
    if (err) return callback(err);
    let results = [];
    let pending = files.length;
    if (!pending) return callback(null, results);
    files.forEach(function(file) {
      const filePath = path.join(dir, file);
      fs.stat(filePath, function(err, stat) {
        if (err) return callback(err);
        if (stat.isDirectory()) {
          processFiles(filePath, function(err, res) {
            if (err) return callback(err);
            results = results.concat(res);
            if (!--pending) callback(null, results);
          });
        } else {
          fs.readFile(filePath, 'utf8', function(err, content) {
            if (err) return callback(err);
            results.push({ path: filePath, content: content });
            if (!--pending) callback(null, results);
          });
        }
      });
    });
  });
}
```

**After** -- clean async/await:

```javascript
import { readdir, stat, readFile } from 'node:fs/promises';
import { join } from 'node:path';

async function processFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const results = await Promise.all(
    entries.map(async (entry) => {
      const filePath = join(dir, entry.name);
      if (entry.isDirectory()) {
        return processFiles(filePath);
      }
      const content = await readFile(filePath, 'utf8');
      return [{ path: filePath, content }];
    })
  );
  return results.flat();
}
```

**Conversion checklist:**
1. Replace `require()` with `import` (ESM) or keep `require` if CommonJS is required
2. Use `node:` prefix for built-in modules (`node:fs`, `node:path`)
3. Replace `fs.readFile(path, cb)` with `await readFile(path)` from `node:fs/promises`
4. Replace manual pending counters with `Promise.all()` or `Promise.allSettled()`
5. Replace `try/catch` around callbacks with `try/catch` around `await`
6. Use `for await...of` for streams instead of `.on('data', cb)`
7. Add `{ withFileTypes: true }` to `readdir` to avoid extra `stat` calls

### 4. Python Script Modernization

**Common upgrades:**

```python
# BEFORE: Python 2/early 3 patterns
import os
import sys
import json

# String formatting
msg = "Hello %s, you have %d items" % (name, count)

# File handling
f = open('data.json', 'r')
data = json.load(f)
f.close()

# Path construction
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.json')

# Subprocess
import subprocess
output = subprocess.Popen(['ls', '-la'], stdout=subprocess.PIPE).communicate()[0]

# Type checking
if type(x) == str:
    pass
```

```python
# AFTER: Modern Python 3.10+
from pathlib import Path
import json
import subprocess
import sys

# f-strings
msg = f"Hello {name}, you have {count} items"

# Context manager
with Path('data.json').open() as f:
    data = json.load(f)

# pathlib
config_path = Path(__file__).parent.parent / 'config' / 'settings.json'

# subprocess.run
result = subprocess.run(['ls', '-la'], capture_output=True, text=True, check=True)
output = result.stdout

# isinstance
if isinstance(x, str):
    pass
```

### 5. Signal Handling and Exit Codes

```bash
# Bash: proper signal handling
cleanup() {
  log "Caught signal, cleaning up..."
  rm -f "$LOCK_FILE"
  exit 130  # 128 + SIGINT(2)
}
trap cleanup INT TERM

# Exit code conventions
# 0 = success
# 1 = general error
# 2 = misuse of shell command (bad args)
# 126 = command not executable
# 127 = command not found
# 130 = terminated by Ctrl+C (128+2)
# 143 = terminated by SIGTERM (128+15)
```

```javascript
// Node.js: graceful shutdown
process.on('SIGINT', async () => {
  console.log('\nReceived SIGINT. Cleaning up...');
  await cleanup();
  process.exit(130);
});

process.on('SIGTERM', async () => {
  console.log('Received SIGTERM. Shutting down gracefully...');
  await cleanup();
  process.exit(143);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught exception:', err.message);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection:', reason);
  process.exit(1);
});
```

## Decision Points

### When to refactor vs. rewrite

| Signal | Action |
|--------|--------|
| Script is < 100 lines and basically works | Refactor in place |
| Script works but has no error handling | Add error handling, keep logic |
| Script uses APIs deprecated 2+ major versions ago | Replace deprecated APIs |
| Script is > 300 lines with tangled control flow | Consider splitting into modules first |
| Script is in a dead language/runtime | Rewrite (but that's a different skill) |
| Script is a critical production tool | Refactor incrementally with tests |

### When to convert CJS to ESM

- **Convert**: New Node.js projects, anything using `type: "module"` in package.json, libraries targeting modern consumers
- **Keep CJS**: Scripts embedded in legacy build systems, anything that must `require()` conditionally, tools with no plans to publish as packages

### Language-specific argument parsers

| Language | Recommended | Why |
|----------|-------------|-----|
| Bash | Manual `case` loop or `getopts` | No dependencies, portable |
| Node.js | `parseArgs` (built-in since Node 18.3) | Zero dependencies |
| Python | `argparse` (stdlib) | Battle-tested, auto-generates help |
| Go | `flag` (stdlib) or `cobra` | Standard practice |

## Anti-Patterns

### 1. Gold-plating a throwaway script
**Symptom**: Adding full argument parsing, logging, and tests to a one-time data migration script
**Fix**: If the script runs once and is deleted, minimal error handling is enough. Save the polish for scripts that live in the repo.

### 2. Replacing `bash` with Node.js for file operations
**Symptom**: Rewriting `cp`, `mv`, `find`, `grep` in JavaScript
**Fix**: Shell is the right tool for file manipulation. Only move to Node.js when the logic (not the I/O) is complex.

### 3. Adding types without adding tests
**Symptom**: Converting a .js script to .ts and calling it "modernized"
**Fix**: Types catch shape errors. Tests catch logic errors. You need both.

### 4. Breaking the interface
**Symptom**: Renaming flags, changing exit codes, or altering output format during a refactor
**Fix**: Refactoring means behavior-preserving changes. If callers depend on the interface, maintain backward compatibility or coordinate the migration.

### 5. Ignoring the shebang
**Symptom**: `#!/bin/bash` on a script that uses bash 4+ features, deployed to macOS (bash 3.2)
**Fix**: Use `#!/usr/bin/env bash` and test on all target platforms. If you need bash 4+, document it.

### 6. Silent failures in pipelines
**Symptom**: `cat file.txt | grep pattern | wc -l` where `file.txt` doesn't exist and the script continues
**Fix**: `set -o pipefail` in bash. In Node.js, check `process.exitCode` after spawning child processes.

### 7. Mixing refactoring with feature additions
**Symptom**: "While I'm in here, let me also add support for..."
**Fix**: One commit for the refactor (behavior-preserving). A separate commit for new features. This keeps the refactor reviewable and revertable.

## Quality Checklist

- [ ] Script has a clear, documented purpose (comment header or `--help`)
- [ ] All arguments are validated with usage errors on bad input
- [ ] `--help` flag works and shows all options
- [ ] Exit codes follow conventions (0 = success, 1 = error, 2 = bad args)
- [ ] No deprecated API calls remain
- [ ] Error messages include context (what failed, what was expected)
- [ ] Signals (SIGINT, SIGTERM) are handled with cleanup
- [ ] Temporary files are cleaned up on exit (trap-based cleanup)
- [ ] No hardcoded paths, credentials, or magic numbers
- [ ] Variables are properly quoted (bash) or validated (Node.js/Python)
- [ ] `set -euo pipefail` is present (bash scripts)
- [ ] Callback chains have been converted to async/await where applicable
- [ ] The script's external interface (flags, exit codes, output format) is unchanged unless intentionally migrated
- [ ] A smoke test or example invocation is documented
