---
name: react-architecture-enforcer
description: Use when fixing bugs, something broken, not working, or doesn't work in React - also when adding features, request says "quick fix", "keep it simple", or "follow existing pattern"
---

# React Architecture Enforcer

## Triggers

**Phrases:** "broken", "not working", "fix", "quick", "simple", "just add", "follow pattern", "match current"

**Context:** Modifying React components, adding features/fixes, file >200 lines, adding hooks

## The Five Laws

| Law | Rule | On Violation |
|-----|------|--------------|
| **A. No Logic in UI** | Components contain NO: prerequisites, credits, progression, scheduling, eligibility | Extract to `/domain`, `/services`, `/config` |
| **B. No Mutating Singletons** | Engines = pure functions or stateless services | Refactor to pure functions |
| **C. No File >300 Lines** | Check `wc -l` before ANY edit | Extract before implementing |
| **D. No Duplicated Logic** | Credits, prerequisites, eligibility = ONE canonical source | Find existing first |
| **E. No Unexamined Effects** | New useEffect requires: justification, dependency audit, store alternative check | Document or reject |

## Pre-Flight (MANDATORY)

1. **Check size:** `wc -l <file>` — >300 lines = HALT
2. **Check pressure words:** `quick`, `simple`, `temporary`, `minimal`, `follow existing` → require extraction plan FIRST
3. **Check logic type:** credits | pathways | prerequisites | GPA | eligibility | scheduling → search existing first

## Rationalization Overrides

| Pattern | Response |
|---------|----------|
| "Pattern exists / follow existing" | Existing violations don't justify new ones. Extract. |
| "It's small / quick / simple" | Size doesn't exempt from laws. Extract. |
| "We'll refactor later" | Requires ticket + sprint + owner. Vague = rejected. |
| "Emergency / production down" | Still output extraction plan (30 sec). Then proceed. |
| "File is already large" | Size IS the problem. No additions without extraction. |

## Extraction Reference

| Logic Type | Extract To |
|------------|-----------|
| Validation | `domain/validators/<name>.js` |
| Calculations | `domain/<name>Calculator.js` |
| Config/Requirements | `config/<name>.config.js` |
| Multiple useState (>3) | `hooks/use<Name>.js` or useReducer |
| Data fetching | `services/<name>Service.js` |
| Scheduling/eligibility | `domain/<Name>Engine.js` |

## Escalation

1. "This violates Law [X]. Extraction required."
2. If user insists → offer minimal extraction path
3. If user overrides → tag code: `// TECH-DEBT: Law X violation [date]`

## Exempt

Comments, formatting, temporary debug logs (removed before commit)
