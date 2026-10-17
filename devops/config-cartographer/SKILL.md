---
name: config-cartographer
description: "Configuration cartographer: maps a system's complete config surface - every env var, setting and flag, where it is defined (.env, yaml/json configs, compose, Dockerfile) versus where it is read in code - and reports read-but-never-defined keys (crash candidates), defined-but-never-read orphans and divergent defaults. Never outputs values, keys only. Read-only. Trigger: /config-map"
trigger: /config-map
---

## What this is for

Configuration sprawl: env vars, settings files, feature flags, in-code defaults spread across .env examples, YAML, JSON, deployment scripts, and code-level reads. Nobody knows the full config surface of a system - which keys exist, where they're defined versus read, which are orphaned or crash-candidates.

**Audience:** Senior
- DevOps uses it to prevent deployment crashes from missing env vars.
- Platform engineers use it for config hygiene across services.
- Anyone debugging "why won't it start locally" scenarios.

### Trigger: `/config-map`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
Print usage block and stop.

### Step 2 - Determine project path
Ask for `-ProjectDir`. Confirm with user.

### Step 3 - Run collector
```powershell
& .\scripts\config-harvest.ps1 -ProjectDir "<path>"
```

### Step 4 - Classify findings
Analyze the JSON output for:
- **Read but never defined** - each env var accessed in code that has no definition in any config source. Check code for fallback (`?? default`, `getenv(..., default)`). Without fallback = crash candidate (high). With fallback = medium.
- **Defined but never read** - orphaned keys (unless they are known runtime keys: NODE_ENV, ASPNETCORE_*, PATH, etc. - filter against a whitelist).
- **Defined multiple times with conflict potential** - same key in multiple sources with unclear precedence.
- **Sensitive without example** - sensitive key (SECRET/TOKEN/KEY/PASSWORD) that exists only in non-example sources, missing from `.env.example`.

### Step 5 - Produce report
Write `config-map-report.md`:

```
# Config Map Report - <project>

## Summary
- <N> definitions in <M> sources, <R> reads in code, <K> distinct keys
- <C> crash candidates (read but never defined)
- <O> orphaned keys (defined but never read)
- <S> sensitive keys without example entry

## Crash Candidates (High Severity)
Key | Reads At | Fallback
... | ... | ...

## Orphaned Keys (Defined, Never Read)
Key | Defined In | Line
... | ... | ...

## Conflict Potential
Key | Sources | Lines
... | ... | ...

## Config Map
Key | Defined In | Type | Sensitive | Read In
... | ... | ... | ... | ...

## Dynamic Reads (Abstraction Gaps)
File | Line
... | ...

## Open Questions
```

### Step 6 - Present
Output the summary to the user. Point to the report file.

## Usage

```powershell
# Interactive
/config-map

# Direct path
/config-map C:\Projects\my-app

# Help
/config-map --help
```

## Important: Never Output Values

The collector discards all secret/configuration values. Only key names, source file paths, line numbers, and metadata (hasValue, sensitive, commented) are emitted. The report MUST NOT contain any concrete configuration values.
