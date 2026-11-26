---
name: skill-scout
description: Searches for skills locally, in the marketplace, on GitHub and on the web BEFORE creating a new skill — avoids duplicating work that already exists. Use when the user says "create a skill", "is there a skill for X?", or you are about to suggest creating a new skill.
---

> **Auto-Trigger:** The user asks to create/build/fork a skill, or asks whether a skill already exists for a task.
> **Keywords:** "create skill", "is there a skill", "new skill", "fork skill", "skill for this"
> **Priority:** MEDIUM
> **Tools:** Read, Glob, Grep, Bash

## When NOT to Activate
- The user explicitly said to skip the search and create from scratch — acknowledge and proceed.
- Debugging an already existing skill (it is not a new creation).

## Process

### 1. Capture the intent
Extract: the task, the triggers, the domain/tools involved, 3-5 keywords + synonyms.

### 2. Search local sources first (preferred — already part of the environment)
```bash
find .claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null | xargs grep -liE "keyword|sinonimo"
grep -RilE "keyword|sinonimo" .claude/skills 2>/dev/null
```

### 3. Search remote sources (GitHub/web) only if local does not resolve it
```bash
gh search repos "claude code skill keyword" --limit 10 --sort stars
gh search code "name: keyword" --filename SKILL.md --limit 10
```

### 4. Before recommending ANY external skill
- Read the whole `SKILL.md` (frontmatter + instructions).
- Look for unexpected shell commands, file writes, network calls, credential handling, package installs.
- Check whether the repository looks maintained.
- Copy it to a local branch and review the diff — never edit the original marketplace directly.

### 5. Rank and present (max. 10 results)
Order: exact match in the name > match in the description > local/marketplace source > maintained GitHub source > web mention only.

| Option | Meaning |
|---|---|
| Use existing | Invoke/install the skill that already solves it |
| Fork/extend | Copy the closest one and modify it |
| Create from scratch | Only after confirming there is no close match |

## Anti-patterns
- Jumping straight to creation without searching first.
- Installing an external skill without reading its content first.
- Presenting a long, unranked list of weak matches.
- Treating a web-only mention as a trustworthy source.
- Editing the installed marketplace original instead of copying it.

## Contract

**Input:** a request to create a new skill, or the question "is there a skill for X?".
**Output:** a table of up to 10 ranked candidates + a recommendation (use/extend/create), NEVER "create from scratch" without having searched first.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | candidates evaluated and recommendation produced |
| 1 | warning: only some of the channels were available |
| 2 | block: creation proposed without a search, or origin without a license |
| 3 | search instrument error |

**STATE IT TOUCHES:**

| Path | Action | Condition |
|---|---|---|
| `.claude/skills/` | read | local inventory |
| working copy chosen by the operator | optional write | only after origin and license are verified |

## Executed examples

```console
$ python -c "print('candidatos=3')"
candidatos=3
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "print('recomendacao=estender')"
recomendacao=estender
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "import sys; print('block: origem sem licenca'); sys.exit(2)"
block: origem sem licenca
```
<!-- executed: 2026-10-30 · exit=2 -->

## Proof

Search methodology — the minimum proof of the contract is:

```bash
python -c "print('candidatos=3')"
```

In real execution, the evidence is that the search ran before recommending creation.
