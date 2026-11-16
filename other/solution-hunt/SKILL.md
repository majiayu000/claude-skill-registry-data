---
name: solution-hunt
description: "Find creative workarounds using local memory and skills. Use when a blocker requires an alternate solution."
---

# /solution-hunt — Creative workaround engine

When blocked, systematically search for legitimate alternate routes before declaring inability.

## Trigger

`/solution-hunt <blocker description>` or `/solution-hunt` (asks for blocker)

## Flow

### 1. Define the blocker
From argument or ask: "What's blocking you?" Get a concrete description of what can't be done and why.

### 2. Search local memory
Grep the vault for related concepts, prior solutions, similar blockers:
```
Grep pattern: {blocker keywords} in $AIGENT_VAULT/
```

### 3. Search local skills
Read `$AIGENT_VAULT/memory/SKILL_LEDGER.md`. Prefix-match against taxonomy paths. Check `memory/SKILL_CHAINS.md` for prior chains that solved similar problems.

### 4. Search GitHub
```
mcp__github__search_repositories: "{blocker} workaround" OR "{blocker} alternative"
mcp__github__search_code: "{specific error or API}" language:typescript OR language:python
```

### 5. Search docs and web
```
mcp__tavily__tavily_search: "{blocker} workaround" OR "{blocker} alternative solution"
mcp__tavily__tavily_extract: {relevant doc URLs found}
```

### 6. Identify 3 routes

| Route | Description |
|-------|-------------|
| **Direct fix** | Solve the root cause — fix the bug, update the dep, change the config |
| **Workaround** | Legitimate alternate path — different API, different tool, decompose the task |
| **Replace component** | Swap the blocking tool/dependency entirely |

### 7. Rank by tradeoffs

| Factor | Weight |
|--------|--------|
| Speed to implement | High |
| Risk of side effects | High |
| Maintainability | Medium |
| Cost (tokens, API calls, money) | Medium |

### 8. Present top 3
For each route, show:
- Description (1-2 sentences)
- Tradeoffs (speed/risk/maintenance)
- Confidence (high/medium/low)
- Implementation steps (3-5 bullets)

### 9. Execute chosen path
On user selection, implement the chosen route. If it requires a new skill, route through `/skill-hunt`.

### 10. Capture learning
- If the solution involved a new pattern: log to `memory/SKILL_CHAINS.md`
- If it exposed a gap: log to `memory/SKILL_GAPS.md`
- If it fixed a recurring issue: log to `memory/FAILURE_MODES.md` via `/learn-from-failure`

## Hard Boundary

> Creative workaround means legitimate alternate route. NEVER:
> - Bypass access controls or authentication
> - Violate terms of service of any platform
> - Exploit security vulnerabilities
> - Hide behavior from the principal
> - Bypass paywalls or rate limits through exploits
> - Use credentials from screenshots or logs

Per [[Capability Expansion Doctrine]] — the authority matrix governs what the AIgent may do. Expansion does not override authority levels.

## Related

- [[concepts/Capability Expansion Doctrine]] — the doctrine this skill serves
- [[memory/SKILL_LEDGER]] — local capability index
- [[memory/SKILL_CHAINS]] — proven multi-skill sequences
- [[memory/FAILURE_MODES.md]] — where failure learnings land
- `/skill-hunt` — external search when local solutions don't exist
- `/learn-from-failure` — structured failure capture
