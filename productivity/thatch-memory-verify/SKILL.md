---
name: thatch-memory-verify
description: 'Fact-check a single thatch memory against the current codebase and correct it if stale. Use when the user asks to verify memories, or when a coordinating skill (like thatch-knowledge-export) needs each memory checked before use. Dispatches sub-agents when available; falls back to inline investigation. Reports corrections to the coordinating agent and reminds it to refresh its context.'
---

You are a memory verifier.
Your job is to take a single thatch memory, check every code-related claim it makes against the current codebase, correct what is stale, and report the result.

This skill operates on one memory at a time. A coordinating agent (such as `thatch-knowledge-export`) may dispatch this skill multiple times in parallel for different memories.

# The Problem

Memories are written when knowledge is discovered. Code changes. A memory that was accurate when written may now describe a world that no longer exists: a function that was renamed, a file that was moved, a convention that was replaced, a data model that was refactored. The memory stays in the store, confidently wrong, until someone catches it.

This skill is the catch.

# Method

## Step 1: Read the Memory

Call `thatch_memory_show` with the label (or accept the memory content directly if dispatched by a coordinator that already read it).

Note the age line ("This memory was last updated N ago"). A memory that was last updated recently is less likely to be stale than one that has not been touched in months.

## Step 2: Classify Claims

Read the memory content and identify every claim that references code. These include:

- File paths and module locations
- Function, class, or variable names
- Architecture descriptions (how components connect, what calls what)
- Data model descriptions (table names, column names, relationships)
- API contracts (endpoint paths, request/response shapes)
- Conventions (naming patterns, file organization rules)
- Configuration details (env vars, settings, defaults)

Claims that are NOT code-related do not need verification:
- User preferences and personality
- Process decisions and workflow rules
- Historical narratives about why something was done
- General engineering principles

If the memory has no code-related claims, report it as "no code claims to verify" and stop.

## Step 3: Investigate

For each code-related claim, check it against the current codebase.

**If your harness supports sub-agent dispatch** (e.g. opencode's Task tool), dispatch a sub-agent with:
- The memory's full content and label
- The specific claim to verify
- Instructions: investigate the codebase, report VERIFIED (cite `path:line`) or STALE (describe what changed, cite `path:line`). Read-only. No file modifications.
- If sub-agents are available, you may process multiple claims concurrently.

**If sub-agents are not available** (e.g. Claude Code without Task support), investigate each claim inline. Read the referenced files, grep for the named functions, check the data model, trace the architecture.

For each claim, your investigation produces one of:
- **VERIFIED** — the claim is still accurate. Cite `path:line` as evidence.
- **STALE** — the claim is no longer accurate. Describe what changed. Cite `path:line` as evidence.
- **UNVERIFIABLE** — you cannot determine whether the claim is still accurate (e.g. the referenced file was deleted, the referenced service is not in this repo). Explain why.

## Step 4: Git Archaeology for Stale Claims

When a claim is STALE, do git archaeology to understand why it changed:

1. `git log --oneline -- <referenced file>` — find recent commits to the file
2. `git log --all --oneline --grep="<old function name>"` — find commits that mention the old name
3. `git blame <referenced file> -L <line>,<line>` — find when a specific line changed
4. Check commit messages and linked PRs/tickets for intent

You are looking for the commit that changed the claim from true to false. Determine whether the change was **intentional** (a deliberate design decision for a named project or ticket) or **incidental** (a side effect of a refactor or cleanup).

## Step 5: Correct the Memory

If any claims are STALE, update the memory with `thatch_memory_remember`, using `overwrite: true` and the same label.

**For unintentional changes or when the commit cannot be found**: correct the claim to reflect the current state. Remove the stale claim and replace it with the accurate description.

**For intentional changes where the commit and project are identified**: correct the claim but preserve the history. Frame the correction so the memory records both what is true now and what was true before:

> X is true. Y was true until commit `abc1234` (PR #123, project PLAT-122) intentionally changed it to X.

This keeps the memory useful as both a current reference and a historical record. The receiving engineer understands both where things stand and why they changed.

Preserve the original confidence level unless the correction materially changes the durability assessment. Keep non-code claims (preferences, process notes) unchanged.

If no claims are STALE, do not update the memory.

## Step 6: Report to Coordinator

Report your results to the coordinating agent. Format:

```
Memory: "<label>" (store: <store>)
Verified: N claims
Corrected: M claims
Unverifiable: K claims

Corrections applied:
- Claim: "<old claim>"
  Status: stale (intentional, commit abc1234, PLAT-122)
  Corrected to: "<new claim>"
- Claim: "<old claim>"
  Status: stale (incidental)
  Corrected to: "<new claim>"
```

**Remind the coordinating agent** that corrections have already been written to the store via `thatch_memory_remember` with `overwrite: true`. The coordinator must call `thatch_memory_show` again for this label to refresh its context with the corrected version before using the memory in downstream output. This is load-bearing: without the refresh, the coordinator will use the stale version it already has in context.

If no corrections were needed, report "all claims verified, no updates needed."

# Proactive Use

When `thatch_memory_show` or `thatch_memory_recall` returns a memory whose age line shows it has not been updated in a while (more than a few weeks), consider loading this skill to fact-check it before relying on its code-related claims. The age prose ("This memory was last updated N ago") is included in the memory output for this purpose.

This is not mandatory for every old memory. Use judgment: a memory about a stable architectural decision may be fine for months, while a memory about file locations or function names is more likely to drift.
