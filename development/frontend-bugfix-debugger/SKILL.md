---
name: frontend-bugfix-debugger
description: 'Diagnose and fix frontend defects from evidence, including unclear UI/runtime errors, broken routes, styling regressions, and hydration or client issues. Reproduce before editing; exclude planned refactors and backend-only debugging.'
id: 'agents.skills.frontend-bugfix-debugger.skill'
title: 'Frontend Bugfix Debugger'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-bugfix-debugger'
tags:
    - 'agents/skill-package'
    - 'frontend/debugging'
    - 'workflow/bugfix'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/debugging-evidence-rules|Debugging Evidence Rules]]'
    - '[[common/agent-loop-policy|Agent Loop Policy]]'
    - '[[common/bounded-retry-rules|Bounded Retry Rules]]'
    - '[[common/verification-loop-rules|Verification Loop Rules]]'
    - '[[common/typescript-discipline|TypeScript Discipline]]'
    - '[[common/lightweight-routing-policy|Lightweight Routing Policy]]'
    - '[[skills/frontend-linter-manager/SKILL|Frontend Linter Manager]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[skills/frontend-quality-reviewer/SKILL|Frontend Quality Reviewer]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Bugfix Debugger

## Purpose

Fix frontend defects from symptoms and evidence while keeping the change small. When verification fails and repair is in scope, use a bounded retry loop instead of guessing repeatedly.

This skill must not turn a one-component presentation defect into a broad debugging, planning, visual QA, or full-repository verification workflow.

## When To Use

Use this skill when the user asks to fix a frontend runtime, console, hydration, routing, rendering, interaction, styling, responsive, TypeScript, or build defect that needs evidence.

Use the Micro UI Fix Fast Lane from `common/lightweight-routing-policy.md` when the defect is an isolated presentation issue that stays within the micro UI hard limits.

## When Not To Use

Do not use this skill for planned refactors, broad quality review, visual QA only, design intake, greenfield planning, backend-only debugging, package installation, or test creation.

If the task is a behavior-preserving refactor, use `frontend-refactor-surgeon`. If the user asks only for review, use `frontend-quality-reviewer`.

If the user only asks for options or an approach, answer with options first and do not edit files until implementation is requested or approved.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read `common/lightweight-routing-policy.md` for micro UI fixes or other narrow code-changing tasks.
4. Read `common/debugging-evidence-rules.md` unless the defect is already explained by a narrow source inspection.
5. Read `common/agent-loop-policy.md`, `common/bounded-retry-rules.md`, and `common/verification-loop-rules.md` only when the user asks to continue until verification passes, repeated failure appears, or bounded retry is needed.
6. Read `common/typescript-discipline.md` for non-trivial TypeScript work.
7. Read relevant project overlays, especially `project/verification-profile.md` and path indexes, only when the task needs repository-specific verification commands or path facts.
8. Read the error, log, route, component, styles, or source files needed for the active bug hypothesis.

For a micro UI fix, default to the context budget in `common/lightweight-routing-policy.md`: owner component, adjacent styles, `package.json` only when dependency presence matters, config only after command failure, and no broad project scans.

## Tool Contract

- May run existing project commands needed to reproduce or verify the symptom.
- May use Browser or Playwright MCP for rendered bug reproduction when available and justified by the task.
- May use `context7` or official docs when current framework behavior affects the fix.
- Activate `openai_platform_docs` only when current OpenAI API or ChatGPT Apps SDK behavior affects the defect or fix.
- May use MDN when browser platform behavior affects the bug.
- Must not install packages, add test workflows, change build tooling, or add UI libraries without explicit approval.
- Must not interact with production systems, secrets, or production data.

For a micro UI fix:

- Do not use `context7` or MDN merely to confirm ordinary rendering-library usage when the project already has examples or installed package metadata.
- Do not inspect MCP installation state.
- Do not start a local server by default.
- Do not invoke Browser or Playwright unless rendered evidence is explicitly requested or required by a named functional acceptance criterion, the route is reachable without new auth/session setup, and navigation tools are available.

## Workflow

1. Classify workflow level and keep one clear bug lightweight.
2. If the user asked for options or approach, answer first and stop before editing until implementation is requested or approved.
3. Determine whether the task qualifies for Micro UI Fix Fast Lane.
4. Record the symptom, reproduction path when available, and current evidence.
5. Form one bug hypothesis and inspect only files relevant to it.
6. Fix the smallest cause that explains the evidence.
7. Preserve existing project conventions, state ownership, accessibility, and TypeScript strictness.
8. Run the same failing command, interaction, route check, or visual check when possible.
9. If verification fails and the failure is related to the current change, apply `common/bounded-retry-rules.md`: record the failed attempt, identify the likely cause, change hypothesis or implementation strategy, avoid repeating the same patch, and retry only within the attempt limit.
10. If verification fails for likely pre-existing or unrelated reasons, document it separately and do not expand scope without approval.
11. Use `frontend-linter-manager` after code-changing work when a lint command exists, except for micro UI fixes where targeted lint/format commands can be run directly without invoking the separate skill.
12. Use `frontend-visual-qa` when the fix changes rendered UI and rendered evidence is required, except for micro UI fixes where source checks plus build/type verification are sufficient unless rendered evidence is explicitly requested or high-risk.
13. Use `frontend-quality-reviewer` when the loop repaired a non-trivial failure or the user asks for review.
14. Report evidence, root cause, fix, verification, attempt count, skipped heavier checks, and any remaining risk.

## Micro UI Fix Verification

For Micro UI Fix Fast Lane, use the verification ladder from `common/lightweight-routing-policy.md`:

1. Changed-file formatting first.
2. Changed-file lint second.
3. Type or build check only when imports, JSX, TypeScript, dependency usage, or bundling behavior changed.
4. Full repository checks only when explicitly requested or when the repository is known clean.
5. Rendered QA only when explicitly requested or high-risk and the route/session/tooling are available.

Do not start a dev server after changed-file checks and build/type verification pass unless rendered evidence is explicitly requested or the fix remains high-risk.

If a full repository command fails with unrelated pre-existing noise, stop broad validation, run the smallest changed-file command if available, and report the pre-existing failure separately.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

```text
Symptom:
Evidence:
Root cause:
Fix:
Attempts:
Verification:
Skipped heavier checks:
Rendered QA:
Remaining risk:
```

## Validation Gates

- The fix must be tied to observed evidence.
- The change must be the smallest scoped correction that addresses the symptom.
- Retry attempts must use new evidence or a changed hypothesis.
- TypeScript safety must not be weakened without explanation and approval.
- Lint verification must run after code changes when a command exists, but micro UI fixes should prefer changed-file lint before full-repository lint.
- UI changes should trigger rendered visual QA only when rendered evidence is required, explicitly requested, or high-risk; micro UI fixes may stop after source checks and build/type verification when sufficient.
- No testing workflow, UI library, package install, or framework migration may be introduced by default.
- No local dev server should be started for a micro UI fix after sufficient source/build evidence unless explicitly justified.

## Trigger Evals

Should trigger:

- "Reproduce and fix this broken route."
- "This UI bug survived the first fix; change the hypothesis and retry."
- "Fix this chat message rendering so already-received markdown displays as markdown, without changing the API."

Should not trigger:

- "Refactor this component without changing behavior."
- "Review this implementation without fixing it."
- "Какими способами можно сделать markdown rendering?"

## Reference Map

- `common/debugging-evidence-rules.md`
- `common/lightweight-routing-policy.md`
- `common/agent-loop-policy.md`
- `common/bounded-retry-rules.md`
- `common/verification-loop-rules.md`
- `common/typescript-discipline.md`
- `project/verification-profile.md`
