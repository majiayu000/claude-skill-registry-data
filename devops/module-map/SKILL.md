---
description: Print a live map of a module — its actions, interfaces, bindings, and cross-module edges
argument-hint: "[module]"
context: fork
agent: Explore
allowed-tools: "Read, Glob, Grep, Bash(ls *), Bash(grep *), Bash(find *)"
---

# Module Map

Summarize the structure of `$ARGUMENTS` (or every module if empty). Read-only orientation before making a change.

## Gather

```bash
find modules/<Module> -name "*.php" | sort
grep -rn "Interface::class" modules/<Module>/*ServiceProvider.php
grep -rn "^use Modules\\\\" modules/<Module> | grep -v "Modules\\\\<Module>\\\\"
```

## Report

```markdown
# <Module>

**Purpose**: <one line>

## Public API
- `<Module>FacadeInterface::method()` — <one line>

## Actions (Application)
| Action | Input → Output | Depends on |
|---|---|---|

## Domain
- Interfaces: …
- DTOs / value objects: …
- Enums: …

## Infrastructure
- Controllers: … (routes they serve)
- Repositories: … (models they touch)

## Bindings
| Interface | Implementation |
|---|---|

## Outbound edges
- <OtherModule> via <Facade> — used by <file>

## Gaps
- Interfaces with no binding
- Classes with no test in tests/Unit/<Module>/
- Any layer violation spotted
```

Keep it scannable — tables and one-liners, no prose narration of the code.
