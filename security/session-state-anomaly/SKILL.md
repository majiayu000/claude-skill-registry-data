---
name: session-state-anomaly
description: "Session state anomaly scanner: finds every session-generation, session-id usage, post-auth session-regeneration, post-logout cleanup, and refresh-token rotation site. LLM per finding: regen? invalidate? rotated? What attack arises if not? Read-only. Audience: Senior. Trigger: /session-anomaly"
trigger: /session-anomaly
---

## What this is for

Missing `session.regenerate()` after login = session fixation attack.
Missing `session.destroy()` after logout = session lingers, hijackable
if token was stolen. Missing refresh-token rotation = long-lived token
window. Generic `security-scan` flags none of these - they require
understanding the session lifecycle per mutation point.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/session-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding per sessionType:

### Step 5

- **creation**: Does the caller call `regenerate` within the next 5 lines?

### Step 6

If not = session fixation risk.

### Step 7

- **login**: Is `regenerate()` called inside the successful auth branch?

### Step 8

If not = session fixation risk.

### Step 9

- **regenerate**: Already present - verify it's in the auth-success path

### Step 10

and not orphaned.

### Step 11

- **logout**: Is `destroy()` / `clearCookie()` / `session.clear()` called?

### Step 12

If not = lingering session risk.

### Step 13

- **jwt/refresh**: Is `rotateRefresh` / `newRefresh` called on refresh?

### Step 14

If not = long-lived refresh token window.

### Step 15

5. Write `session-state-report.md` to the working directory.

## Usage

```
/session-anomaly                            # interactive
/session-anomaly <dir>                      # scan project
/session-anomaly -help                      # show usage
```

Returns JSON with `findings[]`:
`{file, line, sessionType, code, hasRegen, hasInvalidate, hasRotate}`
plus summary counts and `anomalies[]`.
