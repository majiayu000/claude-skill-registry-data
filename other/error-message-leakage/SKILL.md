---
name: error-message-leakage
description: "Error message leakage detector: harvests every HTTP-error-return and log-error-call, classifies what kind of information leaks (stacktrace, SQL error message, env-vars, user input echo, request dump). LLM validates each finding as legitimate production-leak and proposes sanitization. Read-only. Audience: Both. Trigger: /error-leakage"
trigger: /error-leakage
---

## What this is for

Production error-messages leaking stack-traces, SQL queries, file-paths,
secrets, internal IPs. `security-scan` and `security-smell-scanner` mark
generically "don't expose stack traces" - no tool reads the actual
production-return-codes and classifies what exact information reaches
the attacker. This skill catalogs every error-return and log-error call,
and the LLM classifies each as leak-by-info-type.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/error-returns.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- Is this a development-only error path? Does it run in production,

### Step 6

dev-only (NODE_ENV=development), or test-only?

### Step 7

- What information is leaked? (per `leakKind`): stacktrace gives

### Step 8

file-paths+code; SQL error gives schema; env-vars give cloud keys;

### Step 9

user-input echo gives reflection-injection surface.

### Step 10

- Severity scale: stacktrace > SQL error > generic 'Error: X' > request dump.

### Step 11

- Propose sanitization: convert `res.send(err)` to a sanitized error-id,

### Step 12

log full context internally, return generic to caller.

### Step 13

5. Write `error-leakage-report.md` to the working directory.

## Usage

```
/error-leakage                            # interactive
/error-leakage <dir>                      # scan project
/error-leakage -help                      # show usage
```

Returns JSON with `findings[]`:
`{file, line, leakKind, surface, lineContent}` plus summary counts.
