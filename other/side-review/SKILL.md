---
name: side-review
description: Run a lightweight main-conversation to read-only-sidebar review loop with zero-config invocation. Use when `$side-review` is appended to an implementation request, invoked after implementation to create a compact handoff, invoked alone in a fresh task to review the current workspace, or invoked again to rereview prior P1/P2 findings.
---

# Side Review

Infer the next action from conversation and workspace context. Keep the loop human-mediated and stateless. Never use sub-agents. The review phase never modifies project files, Git state, or permissions. Do not let that boundary prevent implementation explicitly requested before the review phase.

## Interpret a bare invocation

- When `$side-review` accompanies a build or change request, complete that authorized implementation and its relevant verification first, then generate a sidebar handoff. Do not review early.
- When invoked after implementation in the same conversation, generate a sidebar handoff without reviewing.
- When invoked in a fresh conversation with an accessible workspace, review immediately. If prior findings exist in this conversation, rereview them.
- Ask only for the project path when no workspace is accessible. Ask for a baseline only when it cannot be inferred safely.

For a fresh Git review, when an upstream merge base is unambiguous, inspect the merge-base-to-`HEAD` committed delta plus staged, unstaged, and untracked changes. Without an unambiguous upstream, inspect staged, unstaged, and untracked changes only when any exist. If the tree is clean or committed work may be in scope, require an explicit baseline; never treat an empty `HEAD` diff as a clean review. Outside Git, require an explicit file scope. Infer intent from available requirements, changed code, tests, and documentation; do not invent missing acceptance criteria.

## Generate a compact handoff

Do not review or edit during handoff generation. Output one copy-ready code block containing only information the sidebar cannot derive:

```text
$side-review
Project: <absolute path>
Scope: <exact files and baseline/range>
Goal: <one short requirement and acceptance summary>
Previous P1/P2: <IDs and fix summary; rereview only>
```

Omit unused lines. Never embed source files or large diffs. Do not repeat this skill's review rules, severity definitions, or finding schema in the handoff.

## Review read-only

Inspect the selected files or Git view, relevant callers, tests, and necessary rendered output from current evidence. Use only operations known not to alter the project, Git, or permissions; isolate safe outputs outside the project or state the limitation.

Report only reachable, reproducible problems supported by a test, trace, code path, render, or concrete scenario. Omit taste, speculation, and unrelated suggestions. Use stable headings such as `SR-001`, preserving IDs on rereview. Under each heading use exactly:

- `severity`
- `location` (file and line)
- `problem`
- `impact`
- `suggested_fix`

Use `P1` for severe breakage, major wrong results, security exposure, or irreversible risk; `P2` for a reachable defect or regression worth fixing now; and `P3` for a non-blocking improvement. Report only useful, evidence-backed P3 findings; omit trivial suggestions. P3 never triggers another round.

If P1/P2 exist, list findings first, then add one compact repair prompt in a complete code block. Include the project, baseline, finding IDs, concise evidence, and explicit approval status. Treat every pending ID as unapproved: require the main conversation to ask once for approval of specific IDs and make no edits until approval is explicit. Then fix only approved P1/P2, preserve unrelated work, verify the fixes, and invoke `$side-review` again. Never include P3 in the repair prompt unless the user explicitly approved that P3 fix.

Use the completion sentence only after fully reviewing the selected scope. If scope, evidence, or access is insufficient, write `Review incomplete: <reason>` instead and never present the limitation as a clean result.

If the review is complete and no P1/P2 exist, optionally list useful P3 findings, then write exactly: “No blocking P1/P2 findings remain; the sidebar review is complete.” Do not generate another prompt.

## Bound rereview

On another bare invocation in the same review conversation, verify prior P1/P2 and check for new P1/P2. Continue only for unresolved or new P1/P2. Stop for repeated failure, no meaningful progress, insufficient evidence, regression, redesign, or broader-scope needs. Never continue indefinitely.
