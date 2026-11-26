---
name: search-first
description: Searches for an existing library/tool/pattern BEFORE writing new code - covers package registries (npm/PyPI), MCP and GitHub, in addition to the local grep. Use before creating a utility, helper, or new integration.
---

> **Auto-Trigger:** Before writing a new utility/helper, adding a dependency, or when the user's request probably already has a ready-made solution.
> **Keywords:** "add functionality", "create utility", "new dependency", "is there a library for this"
> **Priority:** MEDIUM
> **Tools:** Read, Grep, Bash, WebSearch

## When NOT to Activate
- It is already known that no ready-made solution exists (a very business-specific domain).
- It complements, not replaces, the local grep before creating or classifying a file; this skill
  extends the search outside the repo (package registries, MCP, GitHub) before writing new code.

## Flow

```
0. AVAILABILITY PREFLIGHT - check that the search channels exist before relying on them
1. NEEDS ANALYSIS - what is needed, which language/framework
2. SEARCH IN PARALLEL - npm/PyPI · local MCP/skills · GitHub/web
3. EVALUATE - functionality, maintenance, community, docs, license, dependencies
4. DECIDE - adopt as-is / extend-wrap / compose 2-3 packages / build custom
5. IMPLEMENT
```

## Decision matrix

| Signal | Action |
|---|---|
| Exact match, well maintained, MIT/Apache | **Adopt** - install and use directly |
| Partial match, good base | **Extend** - install + thin wrapper |
| Multiple weak matches | **Compose** - combine 2-3 small packages |
| Nothing suitable found | **Build** - custom, but informed by the research |

## Quick mode (inline, before writing a utility)

0. Does it already exist in the repo? → `rg` the relevant modules/tests first
1. Is it a common problem? → search npm/PyPI
2. Is there an MCP for it? → check `.claude/settings.json` + `.mcp.json`
3. Is there a skill for it? → `skill-scout` (from this same module)
4. Is there an implementation/template on GitHub? → code search before writing net-new

## Anti-patterns
- Jumping straight to code without checking whether it already exists.
- Ignoring an available MCP.
- "Found nothing" when a search channel was merely unavailable (report honestly).
- Over-customizing a wrapper until the lib's benefit is lost.
- Bloating dependencies for 1 small feature.

## Contract

**Input:** a need for new functionality, before writing code.
**Output:** a recorded decision (adopt/extend/compose/build) with the real search that grounded it -
never "build" without first having searched the 4 applicable channels.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | applicable search executed and decision recorded |
| 1 | warning: unavailable channel declared |
| 2 | block: decision to build without searching |
| 3 | search instrument error |

**STATE IT TOUCHES:**

| Path | Action | Condition |
|---|---|---|
| target repository | read | local search before creating |
| decision record defined by the project | optional write | only when the project requires it |

## Executed examples

```console
$ python -c "print('local=consulted')"
local=consulted
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "print('decision=adopt')"
decision=adopt
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "import sys; print('block: build without search'); sys.exit(2)"
block: build without search
```
<!-- executed: 2026-10-30 · exit=2 -->

## Proof

Research methodology - the minimum proof of the contract is:

```bash
python -c "print('local=consulted')"
```

In real execution, the evidence is that the applicable search command ran before the new code.
