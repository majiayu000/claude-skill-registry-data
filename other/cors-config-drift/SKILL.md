---
name: cors-config-drift
description: "CORS config drift scanner: harvests every Access-Control-Allow-Origin header, cors()-middleware call, @cross_origin decorator, options-handler with cors config, and per-route origin/credentials settings. LLM analyses each per-route CORS posture: credentials+wildcard = fatal, permissive origin patterns, preflight gaps. Read-only. Audience: Senior. Trigger: /cors-drift"
trigger: /cors-drift
---

## What this is for

CORS configurations drift silently: one route uses `origin:'*'` with `credentials:true`,
another reflects the Origin header, a third forgets preflight handling. Standard scanners
flag "use CORS" - no tool reads the actual per-route origins and credentials and classifies
each as safe vs dangerous. This skill catalogs every CORS-relevant statement, and the LLM
classifies each by drift-type and severity.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/cors-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **Credentials + wildcard**: `origin:'*'` with `credentials:true` is fatally insecure - the browser sends cookies cross-origin to any domain.

### Step 6

- **Permissive origin**: `origin: true` (reflect), regex wildcards like `https://*.example.com` that match unintended subdomains, `allowMultipleOrigins: true`.

### Step 7

- **Preflight handling**: is `OPTIONS` handled? does `Access-Control-Max-Age` expose a large window? are methods/headers overly permissive?

### Step 8

- **Route-specific drift**: one route uses permissive CORS while another on the same app uses restrictive - inconsistent posture across the surface.

### Step 9

- **Header-based vs middleware**: raw `res.header('Access-Control-Allow-Origin', '*')` bypasses any centralized policy - classify as ad-hoc drift.

### Step 10

- Severity scale: credentials+wildcard > reflected origin > regex wildcard > permissive preflight > inconsistent route config.

### Step 11

5. Write `cors-config-drift-report.md` to the working directory.

## Usage

```
/cors-drift                              # interactive
/cors-drift <dir>                        # scan project
/cors-drift -help                        # show usage
```

Returns JSON with `findings[]`:
`{file, line, corsType, origin, credentials, route, wildcard, dangerous}` plus summary counts.
