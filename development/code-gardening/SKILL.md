---
name: code-gardening
description: Synchronize drift in existing repos. Use for stale comments or examples, parser/config errors, pre-existing failures, recurring confusion, or edits to README, plans, SKILL.md, AGENTS.md, CLAUDE.md, generated files, and build/config files. Skip isolated read-only reviews.
---

# Code Gardening

Keep the touched part of an existing codebase trustworthy. Fix cheap, related drift; recover intent where authority is unclear; leave broader uncertainty visible. Keep changes tied to the task. Get the user's approval before rewriting an ambiguous system or starting a broad cleanup. If another skill owns the task, use it as the primary workflow and garden the state it touches. Tiny isolated edits without durable-state impact need no gardening pass.

## Workflow

### 1. Inspect the real boundary

Read each touched file and its nearby callers. Run the actual command, test, parser, build, or validator when feasible; inspect its output. Search the relevant tree for each known-stale identifier or example before editing, so distant matches are counted. Read large, shared, or foundational files in full.

Finish when the affected behavior and every matching stale reference have been located, or the inspection limit is stated.

### 2. Establish authority and scope

Check a baseline early when a failure may predate the task. Prefer observed behavior and passing tests, then tool-native truth (parsers, compilers, `git check-ignore`, generated outputs, schemas), then current docs/specs, then comments. Resolve disagreements with evidence.

Fix small, related drift now: nearby comments or docstrings, renamed examples, style in touched code, missing coupled state, and plan/progress entries named by the task. Surface cross-cutting or behavior-changing drift, uncertain authority, parser/config failures that cannot be fixed confidently in scope, and drift whose fix needs a rewrite or broad cleanup.

Finish when each discrepancy has a supported authoritative source or stated uncertainty, and a fix-or-surface decision.

### 3. Recover intent when needed

When local evidence is inconclusive, follow [archaeology](references/archaeology.md) for history commands and the cold read when its trigger applies. Finish when history clarifies the intended behavior or the remaining ambiguity is explicit.

### 4. Synchronize durable state

For substantial document creation or revision that changes what a reader should do, use the repo-declared authoring skill, or an available `doc-coauthoring` skill when none is declared. Report a missing declared dependency and leave that authoring work pending. Routine synchronization can proceed without an authoring skill.

Update the nearest code, tests, comments, examples, docs, plans, specs, config, build inputs, generated-file policy, and agent guidance affected by a changed fact, vocabulary, workflow, or invariant. For `AGENTS.md`, `CLAUDE.md`, `README`, `SKILL.md`, and long-lived guides, follow [durable-doc editing](references/durable-docs.md). When creating plans or ADRs, changing documented progress, or completing work, use the [document-lifecycle skill](../document-lifecycle/SKILL.md) to reconcile state and retirement under the repo's policy. For human-facing prose, apply `writing-for-humans`.

Finish when every affected surface agrees with the chosen authority, or each remaining mismatch is recorded.

### 5. Validate and hand off

Use the smallest tool-native checks covering the boundary. After a skill edit, run its parser or validator immediately. Compare failures against the baseline, and report which evidence is current versus unverified. Close with a short note of drift fixed, durable state changed, drift remaining, and whether a recurring lesson belongs in agent guidance.

Finish when checks have been inspected and all remaining drift is named.
