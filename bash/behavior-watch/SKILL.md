---
name: behavior-watch
description: >-
  Anomaly detection for AI agent behavior. Monitors tool call patterns,
  file access sequences, and command history to flag unusual activity —
  first-seen patterns, frequency spikes, scope creep, and suspicious
  sequences. Ported from Flare's cloud audit log anomaly detection engine.
  Trigger phrases: "watch my agent", "behavior audit", "what has the agent
  been doing", "session activity report", "anomaly check", "agent activity".
user-invocable: true
allowed-tools: ""
---

# Behavior Watch

Detect anomalous patterns in the agent's own behavior during a session.

## When to Use

- At any point during a session to audit what the agent has been doing
- After a long autonomous run to review the agent's actions
- When something feels off — the agent seems to be doing more than expected
- As a periodic check during sensitive operations

## Methodology

Adapted from Flare's cloud audit log anomaly detection. Instead of analyzing
cloud logs, analyze the agent's own tool call history in this session.

### What to Track

For every tool call in the session, note:

1. **Tool name**: Which tool was called
2. **Target**: File path, URL, command, or search pattern
3. **Direction**: Read (observation) vs Write (mutation)
4. **Scope**: How much of the codebase was touched
5. **Sequence**: What came before and after this call

### Anomaly Signals

Score each signal 0-100, following Flare's scoring guide:
- 85-100 = Critical: immediate attention
- 65-84  = High: worth investigating
- 40-64  = Medium: note and correlate
- 0-39   = Low: informational

**Frequency anomalies:**
- A tool being called far more than expected for the task
  (e.g., 50 Bash calls for a "rename a variable" task)
- Sudden burst of activity after a period of normal pacing
- Repeated failed attempts at the same operation

**Scope anomalies:**
- File access outside the expected working directory
- Reading dotfiles, credentials, or config files unrelated to the task
- Touching files in unrelated parts of the codebase
- Git operations on unexpected branches

**Sequence anomalies:**
- Read credential file → network call (potential exfiltration)
- Write to shell config → Bash execution (potential persistence)
- Read many files rapidly without edits (potential reconnaissance)
- Edit → no test/verify → edit → no test/verify (potential recklessness)

**First-seen patterns:**
- First time accessing a particular directory tree
- First time using a tool not previously used in the session
- First time executing a command pattern not seen before
- Unusual file extensions being read or written

**Task drift:**
- Actions that don't clearly serve the user's stated goal
- Scope expanding beyond what was asked (fixing "related" issues)
- Creating files not requested by the user
- Installing packages or dependencies not discussed

## Report Format

When invoked, analyze the session history and produce:

```
## Behavior Watch Report

Session duration: ~45 minutes
Total tool calls: 67

### Activity Summary
| Tool    | Calls | Read | Write | Notes                    |
|---------|-------|------|-------|--------------------------|
| Read    | 23    | 23   | -     | 4 unique directories     |
| Edit    | 12    | -    | 12    | All in src/components/   |
| Bash    | 18    | -    | 18    | 3 test runs, 2 git ops   |
| Grep    | 8     | 8    | -     |                          |
| Glob    | 4     | 4    | -     |                          |
| Write   | 2     | -    | 2     | New files created        |

### Directories Touched
- src/components/ (34 calls) — primary work area ✓
- src/utils/ (8 calls) — related imports ✓
- tests/ (12 calls) — test execution ✓
- ~/.config/ (2 calls) — ⚠ outside project scope

### Findings

- [MEDIUM] Scope anomaly (score: 52)
  2 Read calls to ~/.config/some-tool/config.json
  These are outside the project directory and not obviously related
  to the task "update the login form."
  Likely benign: checking tool configuration. But worth noting.
  → Suggested action: `/safe-agent:tool-guard profile careful` to gate future
    out-of-scope reads, or `/safe-agent:tool-guard deny Bash` if shell access
    is not needed for this task.

- [LOW] Frequency note (score: 28)
  18 Bash calls is higher than typical for a UI task.
  Breakdown: 8 npm test, 4 npm run build, 3 git status,
  2 git diff, 1 npx tsc. All task-relevant.
  → No action needed.

### Verdict
No critical or high-severity anomalies detected.
All mutations (Edit/Write) are within the expected project scope.
Session behavior is consistent with the stated task.
```

## Remediation Suggestions

Every MEDIUM or higher finding must include a `→ Suggested action:` line recommending
a specific safe-agent skill to mitigate the risk:

| Finding type | Suggested action |
|---|---|
| Scope anomaly (out-of-project access) | `/safe-agent:tool-guard profile careful` or deny specific tools |
| Suspicious sequence (credential + network) | `/safe-agent:tool-guard deny Bash` immediately |
| Excessive tool calls | `/safe-agent:cost-guard $N reject` to cap remaining spend |
| Task drift | Ask the user to confirm the expanded scope |
| First-seen sensitive file access | `/safe-agent:skill-verify` on any recently installed skills |

For LOW findings, add `→ No action needed.` to keep the format consistent.

## Scoring Calibration

To reduce false positives, apply these baseline expectations:

- **Normal read:write ratio**: ~3:1 for typical coding tasks
- **Normal Bash calls**: 5-15 for a focused task, 15-30 for test-heavy work
- **Normal scope**: 2-4 directories for a focused change
- **Expected tools for coding**: Read, Edit, Grep, Glob, Bash — all normal
- **Red flags**: Agent tool, WebFetch, WebSearch used when not requested

Adjust baselines based on what the user asked for. A "refactor the entire
auth module" task justifies more scope than "fix the typo on line 42."

## Limitations

- This skill analyzes the current session only — no cross-session memory
- Tool call history may be compressed in long conversations, limiting
  visibility into early actions
- This is observational analysis, not prevention — it reports what happened,
  it doesn't block future actions (use /tool-guard for that)
