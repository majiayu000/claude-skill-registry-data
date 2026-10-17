---
name: comment-lie-detector
description: "Comment lie detector: extracts every behavioral-claim comment (returns / throws / always / never / must / thread-safe / side-effect) with 30 lines of surrounding code context, then has the LLM judge whether the code does what the comment promises. Categorizes each comment as consistent / contradicts / outdated / unverifiable with confidence proven/likely/suspected. Read-only. Audience: Both. Trigger: /comment-lies"
trigger: /comment-lies
---

## What this is for

Comments are the only part of code nobody tests. They are written once, read
many times, and silently rot. This skill extracts every comment that makes
a verifiable claim about behavior - "returns null on error", "thread-safe",
"never called with empty list", "side-effect-free" - and pairs each with 30
lines of the code it describes, so the LLM can judge whether the code does
what the comment promises.

The dominant failure mode is the load-bearing comment that lies quietly for
months until someone relies on it.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/comment-harvest.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each behavioral claim:

### Step 5

- Read the `codeContext` (30 lines surrounding the comment).

### Step 6

- Does the adjacent code do exactly what the comment states?

### Step 7

- Classify: `consistent` / `contradicts` / `outdated` / `unverifiable`.

### Step 8

5. Confidence: `proven` (direct code evidence), `likely` (multiple lines agree),

### Step 9

`suspected` (inference).

### Step 10

6. Write `comment-lie-report.md` to the working directory.

## Usage

```
/comment-lies                         # interactive, prompts for directory
/comment-lies <dir>                   # scan project directory
/comment-lies -help                   # show usage
```

Returns JSON with `claims[]`: each entry `{file, line, text, kind, codeContext}`
plus `counts: {scannedFiles, totalClaims, byKind}`.

## Report Format

`comment-lie-report.md` with:
- Executive summary (total claims, breakdown by verdict, by file)
- Critical findings (contradicts - the comment actively lies)
- Medium findings (outdated - the comment was true once)
- Low findings (unverifiable - cannot be checked without runtime)
- Consistent claims (benchmark for what good comments look like)
- Confidence column for every finding
- Open questions (suspected, needs human review)
