---
name: autonomous-patching-loop
description: Closed-loop scan → isolate → repair → verify cycle. Agent detects code vulnerabilities or test failures, creates an isolated fix branch, applies auto-remediation, runs the full test gate, and merges only on pass. Inspired by darrenburns/cliche error capture + marionevra/awesome-ai-agents-security playbooks.
origin: darrenburns/cliche (MIT) + marionevra/awesome-ai-agents-security + yamtam feedback-loop.sh
license: MIT
version: 1.0.0
compatibility: bash, git, any project with test suite
---

# autonomous-patching-loop

## When to Use

- A test gate fails and the error is deterministic (TypeError, import error, assertion failure)
- Security scan detects a vulnerability that has a known fix pattern
- CI returns a stack trace that can be mapped to a specific code location
- Triggered by: "auto-fix this", "run the patching loop", "self-heal", "scan and fix", "/smart-fix with isolation"

## Do NOT use for

- Ambiguous failures requiring human design judgment ("make this look better")
- Authentication flows, permission changes, or database migrations — require human review
- Any fix that touches > 5 files (complexity threshold — escalate to human instead)
- Secrets or credential rotation

---

## 4-Phase Loop Architecture

```
Phase 1 — SCAN    Detect failure + extract error location
Phase 2 — ISOLATE Create temporary fix branch (never touch main)
Phase 3 — REPAIR  Apply targeted code fix
Phase 4 — VERIFY  Run full test gate → merge on PASS, loop on FAIL
```

---

## Phase 1: Scan & Error Extraction

```bash
# Capture stderr + stdout, extract actionable error
extract_error() {
  local output="$1"
  # Extract: file path + line number + error message
  echo "$output" | grep -oE '([^[:space:]]+\.(ts|js|py|sh)):([0-9]+)' | head -5
  echo "$output" | grep -iE '(Error|Exception|TypeError|SyntaxError|FAIL|AssertionError).*' | head -10
}

# Run scan and capture
SCAN_OUTPUT=$(bash core/tests/skills/test-skill-triggering.sh 2>&1) || {
  ERRORS=$(extract_error "$SCAN_OUTPUT")
  echo "SCAN FAILED:"
  echo "$ERRORS"
}
```

---

## Phase 2: Isolate (Temp Fix Branch)

```bash
isolate() {
  local issue_id="${1:-auto-$(date +%s)}"
  local branch="fix/temp-agent-patch-$issue_id"

  git stash push -m "pre-patch stash $issue_id" 2>/dev/null || true
  git checkout -b "$branch"
  echo "$branch"
}

# Cleanup on exit
cleanup_branch() {
  local branch="$1"
  local merged="${2:-false}"
  if [[ "$merged" == "true" ]]; then
    git branch -d "$branch" 2>/dev/null || true
  else
    git checkout - && git branch -D "$branch" 2>/dev/null || true
    git stash pop 2>/dev/null || true
  fi
}
```

---

## Phase 3: Repair (Auto-Apply Fix)

```python
# Python: error → fix prompt → apply patch
import subprocess, re, json

def extract_fix_target(error_output: str) -> dict:
    """Extract file and line from stack trace."""
    match = re.search(r'([^\s]+\.(ts|js|py|sh)):(\d+)', error_output)
    if not match:
        return {}
    return {"file": match.group(1), "line": int(match.group(3))}

def apply_fix(file_path: str, error_msg: str, agent_fn) -> bool:
    """Ask agent to fix the file, return True if file changed."""
    with open(file_path) as f:
        content = f.read()
    fixed = agent_fn(f"Fix this error in {file_path}:\n{error_msg}\n\nFile:\n{content}")
    if fixed and fixed != content:
        with open(file_path, "w") as f:
            f.write(fixed)
        return True
    return False
```

---

## Phase 4: Verify + Merge Gate

```bash
MAX_ATTEMPTS=3

patching_loop() {
  local test_cmd="${1:-bash core/tests/skills/test-skill-triggering.sh}"
  local attempt=0
  local branch

  branch=$(isolate "auto-$(date +%s)")

  while [[ $attempt -lt $MAX_ATTEMPTS ]]; do
    attempt=$((attempt+1))
    echo "[patch-loop] Attempt $attempt / $MAX_ATTEMPTS"

    # Run repair (call agent/AI fixer externally, results applied to files)
    # ...repair logic here...

    # Verify
    if $test_cmd 2>&1; then
      echo "[patch-loop] PASS — merging fix into current branch"
      git add -A
      git commit -m "fix(auto-patch): attempt $attempt passed all gates"
      git checkout -
      git merge --no-ff "$branch" -m "merge: auto-patch loop #$attempt"
      cleanup_branch "$branch" "true"
      bash core/scripts/secure-logger.sh "auto-patch" "PASS attempt=$attempt branch=$branch"
      return 0
    fi

    echo "[patch-loop] FAIL — retrying..."
  done

  echo "[patch-loop] EXHAUSTED $MAX_ATTEMPTS attempts — escalating to human"
  cleanup_branch "$branch" "false"
  bash core/scripts/secure-logger.sh "auto-patch" "ESCALATE attempts=$MAX_ATTEMPTS branch=$branch"
  return 1
}
```

---

## CLI Entry Point

```bash
# Run the full patching loop against the skill trigger test suite
bash core/scripts/feedback-loop.sh "bash core/tests/skills/test-skill-triggering.sh" 3

# Or with custom test command
bash core/scripts/feedback-loop.sh "npm test" 5
```

---

## Escalation Triggers

Agent MUST escalate to human (stop the loop) when:

```
□ > 3 consecutive FAIL cycles with the same error
□ Fix touches > 5 files
□ Error is "permission denied" or authentication failure
□ Error involves a missing external dependency (npm package, env variable)
□ Stack trace points to generated/vendor/node_modules code
```

---

## Anti-Fake-Pass Checklist

- [ ] Fix branch created before any edits (never patch directly on main/current branch)
- [ ] Full test gate runs after each repair attempt — not just the failing test
- [ ] Max attempt count enforced (default: 3) — no infinite loops
- [ ] Every attempt logged via `secure-logger.sh` with attempt number + outcome
- [ ] Human escalation fires when max attempts exceeded — agent does not silently give up
- [ ] Branch cleaned up on both success and failure paths
- [ ] Merge only happens after gate PASS — never on partial pass
