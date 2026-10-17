---
name: log-injection-detector
description: "Log injection detector: harvests every console.log/logger.info/log.Error/etc call, classifies arguments for attacker-controlled input (CWE-117), CRLF injection surface, sensitive data leakage (passwords, tokens, secrets). LLM validates each finding as injectable and proposes sanitization (parameterized logging, newline stripping, sensitive-field redaction). Read-only. Audience: Senior. Trigger: /log-injection"
trigger: /log-injection
---

## What this is for

User input flowing into log statements: CRLF-injection (`logger.info(userInput)`),
sensitive data logged (passwords, tokens), log-entries that attacker can forge
via newlines in user content. `data-trail-tracker` finds where PII lands;
doesn't surface CWE-117 log-injection attack vectors. This skill catalogs every
log-statement call, classifies each argument for injection risk, and proposes
sanitization per finding.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/log-arg-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **Has user input?** Does the log call include `req.body`, `req.query`,

### Step 6

`req.params`, `input`, `event.body`, `message.body`, or any directly

### Step 7

passed HTTP request-derived variable?

### Step 8

- **CRLF injection possible?** Is the argument unsanitized - concatenated

### Step 9

with `+`, template-literal-interpolated with variables, passed raw to

### Step 10

`logger.info(userVar)` - allowing attacker-controlled line breaks?

### Step 11

- **Sensitive data leaked?** Do arguments contain keywords like `password`,

### Step 12

`secret`, `token`, `key`, `auth`, `session`, `cookie`, `credit`, `ssn`,

### Step 13

`email` - data that forensic attackers would harvest from log files?

### Step 14

- **Payload impact:** What can attacker achieve via forged log entries?

### Step 15

(log-poisoning, SIEM-alert evasion, incident-response misdirection,

### Step 16

credential harvesting from logs.)

### Step 17

5. Write `log-injection-report.md` to the working directory.

## Usage

```
/log-injection                            # interactive
/log-injection <dir>                      # scan project
/log-injection -help                      # show usage
```

Returns JSON with `findings[]`:
`{file, line, callText, hasUserInput, hasSensitiveData, userInputSources[],
sensitiveKeys[], unsanitizedPlus, unsanitizedTemplate, hasCRLFRisk}` plus
summary counts.
