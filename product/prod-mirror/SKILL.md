---
name: prod-mirror
description: "Production behavior mirror: ingests exported log files (text or JSON lines), statistically condenses them (frequencies, error rates, hot paths), extracts the code's expectations (log statements, catch blocks, routes), then has the LLM report the deltas - dead features, swallowed errors firing daily, unexpected hot paths. Works fully offline on exported logs. Read-only. Trigger: /mirror"
trigger: /mirror
---
# /mirror

What your code promises and what prod actually does are two different stories.
Matches exported logs statistically against code expectations: dead features,
swallowed errors, unexpected hot paths, "impossible" states that fire anyway.

## What this is for

- Nobody knows production reality completely; decommission/prioritization decisions
  are based on opinion instead of evidence. Works fully offline on exported
  log files (text or JSON lines) - no live connection to
  observability platforms.
- **Read-only skill.** No PII processing: email addresses and long
  digit sequences are masked in ALL output, not just in examples.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked

If `/mirror -help` or `/mirror -h` (without further arguments) is invoked:
output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir` (code), `-LogDir` (exported logs) and a rough estimate
of the log time period (free text, for context in the report). Get confirmation.

### Step 3 - Collect evidence

```powershell
& "<SKILL_DIR>/scripts/log-ingest.ps1" -LogDir "<logdir>"
& "<SKILL_DIR>/scripts/code-claims.ps1" -ProjectDir "<path>"
```

Empty/missing LogDir: the script aborts with exit code 1 (without logs the
comparison is pointless) - forward message, stop.

### Step 4 - Compare in four directions

Actively perform each direction, do not just note what catches your eye:

1. **Code expects, logs silent** -> dead feature candidates: routes and
   log messages whose patterns do not appear in the logs. Caution: log level
   may be filtered in prod - check if ANY info lines exist in the log;
   otherwise limit this direction to error/warn and note the limitation.
2. **Logs scream, code swallows** -> error patterns with high frequency whose
   origin is a `swallowGuess` catch or a log without further handling -
   the "quiet constant fires". Map via message literal similarity (exact
   > normalized > semantic; confidence accordingly `proven`/`likely`/
   `suspected`).
3. **Unexpected hot paths** -> top patterns by frequency whose code locations
   appear inconspicuous (retry loops, fallbacks) - name what the frequency
   reveals about system behavior.
4. **"Impossible" states** -> log patterns with "should never happen" character
   (message contains never/unreachable/unexpected/impossible) that nevertheless
   fire countably.

Logs from another service (mapping ratio ~0): warn "Logs may not
match the project" instead of fabricating nonsense deltas.

### Step 5 - Write report

File `mirror-report.md` in the current working directory:

1. **Summary** - metrics + 3 most important deltas.
2. The four delta categories with evidence (log pattern + count + time period,
   code location `file:line`).
3. **Recommendations** - concrete ("catch in X:123 does not log - error for 6 weeks
   8123x").
4. **Open questions** - all `suspected` mappings, log level limitations.

Evidence requirement: each delta needs BOTH sides (code location AND
log statistics) or is labeled as one-sided.

### Step 6 - Summarize

State the report path, summarize the 3 most important deltas directly in chat.

## Usage

```
/mirror                          # interactive
/mirror <repo> <logdir>          # compare code vs. logs
/mirror -help
```


