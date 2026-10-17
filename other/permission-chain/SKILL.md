---
name: permission-chain
description: "Permission chain analyzer: extracts role definitions, role check sites, middleware mounts, and mutating routes. Identifies transitive chains (role A can reach endpoint E via routes R1,R2...), surfaces unprotected mutating routes (file-local check missing), detects divergent role-naming (same role defined differently in 3 files). Read-only. Audience: Senior. Trigger: /permission-chain"
trigger: /permission-chain
---

## What this is for

`if(user.role=='admin')` at one site is not the problem. Five such checks
across 3 roles plus middleware inheritance is the problem - who can do
WHAT, transitively. `authorization-xray` builds the permission matrix per
route. Missing: transitive closure, divergent-set detection, and unprotected
mutating routes where the only protection is middleware inheritance.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/permission-graph.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **Unprotected mutating route** (no check within +/-40 lines): does it

### Step 6

inherit from middleware? what is the abuse path if middleware fails?

### Step 7

- **Divergent role set**: 4 files define `admin` differently. Is one

### Step 8

the intended truth? Where is the mismatch?

### Step 9

- **Diamond chains**: same role reaches endpoint via two paths with

### Step 10

different truth-values.

### Step 11

- **Broken chain** (set-without-verify): role gets set in middleware but

### Step 12

no check ever compares against it.

### Step 13

5. Write `permission-chain-report.md` to the working directory.

## Usage

```
/permission-chain                           # interactive
/permission-chain <dir>                     # scan project
/permission-chain -help                     # show usage
```

Returns JSON with `roleDefines[]`, `roleChecks[]`, `middleware[]`,
`mutatingRoutes[]`, `unprotectedRoutes[]`, `knownRoles[]` plus summary counts.
