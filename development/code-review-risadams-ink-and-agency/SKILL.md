---
name: code-review
category: codebase-build
description: >
  Two-axis review of the working diff since a fixed point — Standards (repo conventions and
  code smells) and Spec (matches the originating ticket). Use when the user wants to review
  a branch or work-in-progress changes, says "review since X", or asks for a pre-MR review.
codex-short-description: "Two-axis (Standards + Spec) review of the working diff"
compatibility: claude-code codex opencode
---

# Code Review

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards (plus a code-smell baseline)?
- **Spec** — does the code faithfully implement the originating ticket / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

> **Not `mr-review`.** This reviews your **working diff** (local branch, pre-MR) against a fixed point, using two focused axes. `mr-review` / `mr-gatekeep` review a **posted GitLab MR** for process compliance and sign-off. Reach for `code-review` while building; `mr-review` once the MR is up.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`. If they didn't specify, ask. Capture the diff once: `git diff <fixed-point>...HEAD` (three-dot, against the merge-base), and the commit list via `git log <fixed-point>..HEAD --oneline`.

Confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty **before** spawning sub-agents — a bad ref or empty diff should fail here, not inside them.

**Committed work only.** `...HEAD` is measured from the merge-base and excludes staged and working-tree changes, so anything not yet committed is invisible to both axes. Check `git status --porcelain` first; if the tree is dirty, say which files are unreviewed and offer to commit (or review `HEAD` plus a separate pass over the working tree) rather than silently reviewing a subset of the work.

### 2. Identify the spec source

In order: (1) issue references in commit messages (`PRJ-123`, `Closes #45`, GitLab `!67`) — fetch via Jira/GitLab MCP; (2) a path the user passed; (3) a spec under `docs/`, `specs/`, or a Confluence page matching the branch/feature; (4) if nothing, ask. If there's no spec, the Spec axis skips and reports "no spec available".

### 3. Identify the standards sources

Anything documenting how code should be written here — `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CONTEXT.md`. On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — Fowler code smells (*Refactoring*, ch.3) that apply even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*:

- **Mysterious Name** — a name that doesn't reveal what it does/holds. → rename; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape in more than one hunk/file. → extract, call from both.
- **Feature Envy** — a method reaching into another object's data more than its own. → move it onto the data it envies.
- **Data Clumps** — the same few fields/params travelling together. → bundle into one type.
- **Primitive Obsession** — a primitive standing in for a domain concept. → give the concept its own small type.
- **Repeated Switches** — the same switch/if-cascade on the same type recurs. → polymorphism, or one shared map.
- **Shotgun Surgery** — one logical change forces scattered edits. → gather what changes together into one module.
- **Divergent Change** — one module edited for several unrelated reasons. → split so each changes for one reason.
- **Speculative Generality** — abstraction/hooks for needs the spec doesn't have. → delete; inline until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation. → hide the walk behind one method.
- **Middle Man** — a class/function that mostly just delegates. → cut it, call the target direct.
- **Refused Bequest** — a subclass ignoring most of what it inherits. → drop inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` (`general-purpose`) calls.

**End both briefs with:** *"Perform this review directly. Do not invoke the `code-review` skill and do not spawn further agents."* Without it a sub-agent can rediscover this skill from its own listing and fan out again, and the recursion compounds — it is the one failure here that gets expensive rather than merely wrong.

**Standards sub-agent** — include the full diff command + commit list, the standards-source files from step 3, **plus the smell baseline pasted in full** (the sub-agent has no other access to it). Brief: *"Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard; and (b) any baseline smell: name it and quote the hunk. Distinguish hard violations from judgement calls — documented breaches can be hard, baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."*

**Spec sub-agent** — include the diff command + commit list and the spec path/contents. Brief: *"Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but wrong. Quote the spec line for each finding. Under 400 words."* If the spec is missing, skip this sub-agent and note it.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec`, verbatim or lightly cleaned. **Do not merge or rerank** — the axes are deliberately separate. End with a one-line summary: total findings per axis and the worst issue *within each axis*. Don't pick a single winner across axes.

## Why two axes

A change can pass one and fail the other — code that follows every standard but implements the wrong thing (Standards pass, Spec fail), or code that does exactly what was asked but breaks conventions (Spec pass, Standards fail). Reporting them separately stops one axis from masking the other.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Both axes reported separately — Standards findings never merged into Spec findings, or vice versa
- Every finding cites a concrete location (file:line) and the rule or spec clause it violates
- Spec axis actually references the originating ticket/spec, not just inferred intent
- No finding is a false positive from unreviewed generated or vendored code

> **Host portability:** tool names follow Claude Code conventions; on other hosts map by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/code-review.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
