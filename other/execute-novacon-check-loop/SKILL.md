---
name: execute
description: Executes approved multi-step plans when they need isolated implementation workers, repository-native validation, and adversarial review before commit or push.
argument-hint: "[plan-path]"
---

# Supervised plan execution

## Overview

The orchestrator owns the plan, validation, and every decision. A fresh subagent implements or fixes one bounded step. The configured Codex reviewer reviews each step in one persistent read-only thread. `codex-invoke.mjs step` runs the mechanics: it snapshots the working tree without staging, computes the step-scoped diff, omits protected paths, redacts secrets, builds the reviewer prompt, numbers findings (`S1`, `S2`, ...), keeps the ledger, sends only the fix delta on re-review, and caps each step at three fix attempts.

**Core principle:** No evidence, no blocking finding. Review output is a claim until the orchestrator checks its cited source.

Do not commit or push before explicit user approval.

## Prepare

Treat `$ARGUMENTS` as the approved plan path. If it is empty, use the single plan active in the conversation or repository. Ask only when no single plan can be identified.

Read the complete plan, the original request, the repository instruction files, and the build, test, lint, and type-check commands from repository configuration. Lock the plan: a wrong or impossible step needs user input, not a silent rewrite.

This skill runs on the session's current model and effort; it does not switch models.

**In pi:** pi does not substitute `${CLAUDE_PLUGIN_ROOT}`; replace it with the absolute path two directories above this SKILL.md. `$ARGUMENTS` is the text appended after `/skill:execute`.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" setup --cwd "$(pwd)"
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" config --cwd "$(pwd)"
```

Proceed only on `Status: ready`. `config` prints `model`, `effort`, `maxRounds`, and `implementerModel`. The first review turn freezes the reviewer model and effort for the execution; an explicit model or effort that is unavailable or substituted fails rather than switching reviewers. `maxRounds` does not apply here: every step gets one review plus at most three fix re-reviews. `implementerModel` null means implementers inherit the session model.

### Working-tree ownership

Run `git status --porcelain`. If anything is listed, ask the user to choose before touching files:

1. Execute in an isolated worktree created from HEAD, leaving the dirty tree untouched.
2. Explicitly include the named existing changes in this execution.

Never hide, discard, stage, or silently include existing work. Never present baseline work as implementer output. Keep all execution changes uncommitted until final approval.

## Each step

Process steps in order. One step owns one implementation and review loop.

### 1. Record the base, then implement

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" step --cwd "$(pwd)" --plan PLAN_PATH --step N --begin
```

This must run before the implementer. The first `--begin` of an execution also records the execution base. Add `--new` only to abandon a previous execution of the same plan.

Write the step contract: the exact plan text, allowed files or subsystem, dependencies from completed steps, observable acceptance criteria, and the validation commands for this step. Dispatch one fresh subagent with `./implementer-prompt.md`:

```text
Agent tool:
  subagent_type: "general-purpose"
  model: IMPLEMENTER_MODEL   # omit when implementerModel is null
```

In pi, use the `subagent` tool with `agent: "worker"` and `context: "fresh"`, and pass `model` as the configured `implementerModel` or the session's current provider/id. If an explicit `implementerModel` is rejected or unavailable, stop and report it rather than substituting another model.

Handle the implementer's status: `DONE` continue; `DONE_WITH_CONCERNS` resolve the concerns first; `NEEDS_CONTEXT` gather it and dispatch a fresh subagent; `BLOCKED` change the context or decomposition, and ask the user if the plan itself is wrong. Never retry an unchanged prompt after a blocker, and never run overlapping implementers.

### 2. Inspect and validate

Read the changed files against the contract. Confirm unrelated user changes are untouched. Run the smallest repository-native commands that prove this step, exercise the changed surface when a runtime exists, and record exact output. Fix validation failures with a fresh fixer before review, giving it the exact failure output; after three unsuccessful validation-fix attempts, stop and ask the user.

### 3. Review

Write the contract to a file and the observed validation output to another, then:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" step --cwd "$(pwd)" --plan PLAN_PATH --step N \
  --contract-file CONTRACT_FILE --validation-file VALIDATION_FILE
```

The runner diffs the working tree against the recorded base, drops files matching `*.env*`, `*.secret*`, `*credentials*`, and `**/secrets/**`, redacts credential-shaped values, and sends the packet in the persistent thread. On the first step it also sends the plan. The result is one JSON object:

```json
{"status":0,"error":null,"round":1,"maxRounds":4,"next":"adjudicate","summary":"Round 1/4: 1 new blocker(s) (S1).","blockers":[...],"notes":[...],"questions":[],"reviewer":{"model":"...","effort":"..."},"omittedProtectedPaths":[],"runFile":"..."}
```

Show the user only `summary`. If `omittedProtectedPaths` is nonempty, say which paths the reviewer did not see.

| `next` | Action |
|---|---|
| `adjudicate` | Adjudicate every blocker, fix, re-run validation, call `step` again with the adjudication and fresh validation. |
| `adjudicate-final` | Same, but this was the last fix attempt. |
| `stalled` | The same blockers survived two rounds or a confirmed fix came back. Ask the user: *Keep fixing*, *Waive these risks*, or *Stop here*. |
| `cap` | Three fix attempts are spent with fixes unreviewed. Ask the user: *Accept as is* or *Stop here*. |
| `done` | The step is complete. |
| `retry` | The reviewer turn failed; nothing was recorded. Rerun the identical command once, then stop with the error. |

A nonzero exit or `status: 1` is never a review result and never approval.

### 4. Adjudicate

Only `VERIFIED` critical or important findings arrive as blockers. For each one, open the cited location, confirm it exists, is current, and supports the exact claim and failure condition, then decide:

- `ACCEPT`: verified defect; the proposed correction is right.
- `REJECT`: contradicted, unsupported, irrelevant, or preference-only.
- `COUNTER`: verified defect; a different correction is safer or simpler.
- `WAIVE`: only when the user explicitly accepts the risk; name that decision in the reason.

Model agreement, severity, confidence, and repetition are not evidence. `notes` and `questions` never block; act on a question only when the answer is verified and material.

For accepted and countered findings, dispatch one fresh fixer with the current contract, the verified finding, and the chosen correction only. Re-run validation. Then continue:

```json
{"decisions":[{"id":"S1","decision":"ACCEPT","reason":"src/a.js:12 confirmed; bound corrected."}]}
```

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" step --cwd "$(pwd)" --plan PLAN_PATH --step N \
  --adjudication-file DECISIONS_FILE --validation-file VALIDATION_FILE
```

The runner refuses a decision set that misses a pending ID or lacks a reason, and refuses to continue if you accepted a finding but the tree is unchanged. It sends only the delta since the last review. If every blocker is rejected or waived, the step converges without another reviewer turn.

### 5. Report the step

```text
Step N: COMPLETE
Implementation: IMPLEMENTER_MODEL or session model
Validation: commands and outcomes
Codex (model, effort): outcome from `summary` [after N fix attempts]
Adjudication: accepted S... | rejected S... | countered S...
Open questions: S... or none
```

Continue to the next step without committing.

## Final verification

After the last step, run the repository's full validation and exercise the final surface. Review everything since the execution base:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" step --cwd "$(pwd)" --plan PLAN_PATH --step final \
  --contract-file FINAL_CONTRACT_FILE --validation-file VALIDATION_FILE
```

The final contract is the locked plan's acceptance criteria. Adjudicate and fix exactly as for a step; after each accepted fix, re-run full validation.

## Final approval gate

Present the plan path and base commit, completed steps, changed files, exact validation commands and outcomes, runtime evidence, the accepted, rejected, and countered findings, open questions and residual risks, the final review outcome with actual model and effort, and `git status`.

If the user cancels, stop, leave every change visible and uncommitted, and report `CANCELLED — NOT APPROVED`. Otherwise ask whether to commit and push. Until the user explicitly approves, do neither. If approved, create only the requested commits and push only the requested branch.

## Common mistakes

| Mistake | Correct action |
|---|---|
| Reviewing without `--begin` | The runner refuses; record the base before the implementer runs. |
| Letting an implementer stage or commit | Keep git ownership with the orchestrator. |
| Hiding a dirty tree | Ask for isolation or explicit inclusion. |
| Accepting a severe finding on confidence | Open its evidence. |
| Treating two-model agreement as proof | Verify the source and failure condition. |
| Hand-building reviewer prompts with `turn` | Use `step`; it owns the diff, filtering, and ledger. |
| Reusing an implementer context | Dispatch a fresh subagent for each implementation or fix. |
| "Codex withheld approval, so the hypothesis blocks." | Completion depends on verified blockers, not wording. |
